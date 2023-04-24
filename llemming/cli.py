import argparse
import glob
import os

from . import hone
from .settings import MODELS
from .version import VERSION


def handle_hone(args: argparse.Namespace) -> None:
    ignores = set()
    if args.ignores_file is not None:
        with open(args.ignores_file, "r") as ifp:
            for line in ifp:
                stripped_line = line.strip()
                if stripped_line == "" or stripped_line.startswith("#"):
                    continue
                for item in glob.glob(stripped_line, root_dir=args.dir):
                    ignores.add(os.path.join(args.dir, item))
                if "*" not in stripped_line:
                    for item in glob.glob(f"**/{stripped_line}", root_dir=args.dir):
                        ignores.add(os.path.join(args.dir, item))
    if os.path.exists(os.path.join(args.dir, ".git")):
        ignores.add(os.path.join(args.dir, ".git"))
    if args.prompt:
        prompt = hone.generate_prompt(
            directory=args.dir, ignores=ignores, symlinks=args.symlinks
        )
        print(prompt)
    else:
        result = hone.hone(
            model=args.model,
            directory=args.dir,
            ignores=ignores,
            symlinks=args.symlinks,
        )
        print(result)


def generate_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="llemming")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=VERSION,
        help="Show llemming version",
    )
    parser.set_defaults(func=lambda _: parser.print_help())

    subparsers = parser.add_subparsers(
        title="Commands", description="llemming commands"
    )

    hone_help = "Identify files in a code base to analyze more deeply"
    hone_command = subparsers.add_parser("hone", help=hone_help, description=hone_help)
    hone_command.add_argument(
        "--model", required=True, choices=MODELS(), help="OpenAI model to use"
    )
    hone_command.add_argument("-d", "--dir", required=True, help="Directory to analyze")
    hone_command.add_argument("--ignores-file", help="File to read ignores from")
    hone_command.add_argument(
        "-s",
        "--symlinks",
        action="store_true",
        help="Set this flag to follow symbol links to directories",
    )
    hone_command.add_argument(
        "--prompt",
        action="store_true",
        help="If you set this flag, this command prints the prompt and exits without actually executing the model.",
    )
    hone_command.set_defaults(func=handle_hone)

    return parser


def main() -> None:
    parser = generate_argument_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
