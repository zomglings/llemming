from dataclasses import dataclass, field, asdict
import os
import textwrap
from typing import Any, Dict, List, Optional, Set

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from .settings import OPENAI_API_KEY


@dataclass
class Directory:
    subdirs: List[str] = field(default_factory=list)
    files: List[str] = field(default_factory=list)


def dirtree(
    directory: str,
    only_extensions: Optional[List[str]] = None,
    ignores: Optional[Set[str]] = None,
    symlinks: bool = False,
) -> Dict[str, Any]:
    """
    Return a data structure representing the filesystem tree under the given directory
    """
    if only_extensions is not None:
        extensions = [
            extension for extension in only_extensions if extension[0] == "."
        ] + [f".{extension}" for extension in only_extensions if extension[0] != "."]

    ignores_absolute = set()
    if ignores is not None:
        ignores_absolute = {os.path.abspath(item) for item in ignores}

    tree = {}
    for root, dirs, files in os.walk(directory, followlinks=symlinks, topdown=True):
        for subdir in dirs:
            if os.path.abspath(os.path.join(root, subdir)) in ignores_absolute:
                dirs.remove(subdir)
        if os.path.abspath(root) in ignores_absolute:
            continue
        valid_files = [
            file
            for file in files
            if os.path.abspath(os.path.join(root, file)) not in ignores_absolute
        ]
        if only_extensions is not None:
            unignored_files = [*valid_files]
            valid_files = []
            for file in unignored_files:
                _, ext = os.path.splitext(file)
                if ext in extensions:
                    valid_files.append(file)

        tree[root] = Directory(
            subdirs=[os.path.join(root, dir) for dir in dirs], files=valid_files
        )
    return tree


def render_dirtree(dirtree: Dict[str, Any], base: str, indent: int = 2) -> str:
    """
    Renders a directory tree as a string
    """
    current_dir = dirtree.get(base)
    if current_dir is None:
        return ""

    dirname = base
    if dirname[-1] != "/":
        dirname += "/"

    subdir_renders_raw = [
        render_dirtree(
            dirtree=dirtree,
            base=subdir,
            indent=indent,
        )
        for subdir in current_dir.subdirs
    ]
    subdir_renders = [
        textwrap.indent(raw, prefix="|" + " " * indent)
        for raw in subdir_renders_raw
        if raw != ""
    ]
    file_renders = [f"|- {filename}" for filename in current_dir.files]

    render = "\n|\n".join([dirname, *subdir_renders, *file_renders])

    return render


DESCRIBE_DIRECTORY_PROMPT = """I am interested in learning more about a directory with the following tree structure:
{directory}

Please answer two questions for me:

1. Topics: Can you explain to me the different high-level, semantic topics that the files in the directory represent? Include a description of each topic. Return the topics as a list in the form:

2: Entrypoints: Which files would be good entrypoints to each of the different topics?

Please return your answer in JSON format, in the following structure:
{{
    "topics": {{"<high level topic 1>": "<description of topic 1>", "<high level topic 2>": "<description of topic 2>", ...}},
    "entrypoints": {{"<high level topic 1>": ["<entrypoint 1 for topic 1>", "<entrypoint 2 for topic 1>", ...], "<high level topic 2>": ["<entrypoint 1 for topic 2>", "<entrypoint 2 for topic 2>", ...], ...}}
}}

Remember, the topics should reflect the high-level semantics of the files in the directory.

Thank you for your help!
"""


def analyze_directory(
    directory: str,
    only_extensions: Optional[List[str]] = None,
    ignores: Optional[Set[str]] = None,
    symlinks: bool = False,
) -> str:
    tree = dirtree(
        directory=directory,
        only_extensions=only_extensions,
        ignores=ignores,
        symlinks=symlinks,
    )
    render = render_dirtree(tree, directory)

    llm = OpenAI(openai_api_key=OPENAI_API_KEY())
    prompt = PromptTemplate(
        input_variables=["directory"], template=DESCRIBE_DIRECTORY_PROMPT
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    result = chain.run(render)
    return result
