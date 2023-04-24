from dataclasses import dataclass, field, asdict
import os
import textwrap
from typing import Any, Dict, List, Optional, Set

import openai

from .settings import OPENAI_API_KEY


# Set OpenAI API key
openai.api_key = OPENAI_API_KEY()


@dataclass
class Directory:
    subdirs: List[str] = field(default_factory=list)
    files: List[str] = field(default_factory=list)


def dirtree(
    directory: str,
    ignores: Optional[Set[str]] = None,
    symlinks: bool = False,
) -> Dict[str, Any]:
    """
    Return a data structure representing the filesystem tree under the given directory
    """
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


DESCRIBE_DIRECTORY_PROMPT = """We have to analyze a codebase in a directory with the following tree structure:
{dirtree}

Our goal at the end of our work is to generate high-level documentation about the code in this codebase.

Which files should we start by analyzing? For each file, please provide a list of topics you think that
file could pertain to.

Return your output as a list of files to analyze, along with expected topics:
- file_1,topic_1_1,...,topic_1_{{n_1}}
- file_2,topic_2_1,...,topic_2_{{n_2}}
- ...

Each file should be specified as a path relative to the root of the codebase.
"""


def generate_prompt(
    directory: str,
    ignores: Optional[Set[str]] = None,
    symlinks: bool = False,
) -> str:
    tree = dirtree(
        directory=directory,
        ignores=ignores,
        symlinks=symlinks,
    )
    rendered_tree = render_dirtree(tree, directory)

    prompt = DESCRIBE_DIRECTORY_PROMPT.format(dirtree=rendered_tree)

    return prompt


def hone(
    model: str,
    directory: str,
    ignores: Optional[Set[str]] = None,
    symlinks: bool = False,
) -> str:
    prompt = generate_prompt(directory, ignores, symlinks)

    result = openai.Completion.create(model=model, prompt=prompt, max_tokens=1000)

    return result
