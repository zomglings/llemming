from dataclasses import dataclass, field, asdict
import os
import textwrap
from typing import Any, Dict, List, Optional

from langchain.llms import OpenAI


@dataclass
class Directory:
    subdirs: List[str] = field(default_factory=list)
    files: List[str] = field(default_factory=list)


def dirtree(
    directory: str, only_extensions: Optional[List[str]] = None, symlinks: bool = False
) -> Dict[str, Any]:
    """
    Return a data structure representing the filesystem tree under the given directory
    """
    tree = {}
    for root, dirs, files in os.walk(directory, followlinks=symlinks, topdown=True):
        valid_files = files
        if only_extensions is not None:
            extensions = [
                extension for extension in only_extensions if extension[0] == "."
            ] + [
                f".{extension}" for extension in only_extensions if extension[0] != "."
            ]
            valid_files = []
            for file in files:
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
    dirname = base
    if dirname[-1] != "/":
        dirname += "/"

    current_dir = dirtree[base]

    subdir_renders = [
        textwrap.indent(
            render_dirtree(
                dirtree=dirtree,
                base=subdir,
                indent=indent,
            ),
            prefix="|" + " " * indent,
        )
        for subdir in current_dir.subdirs
    ]
    file_renders = [f"|- {filename}" for filename in current_dir.files]

    render = "\n|\n".join([dirname, *subdir_renders, *file_renders])

    return render


def analyze_directory(
    directory: str, only_extensions: Optional[List[str]] = None, symlinks: bool = False
) -> None:
    # llm = OpenAI()
    tree = dirtree(
        directory=directory, only_extensions=only_extensions, symlinks=symlinks
    )
    render = render_dirtree(tree, directory)
    print(render)
