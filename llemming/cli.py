import argparse
import glob

from .analyze_directory import analyze_directory
from .version import VERSION


def handle_analyzedir(args: argparse.Namespace) -> None:
    ignores = set(args.ignores) if args.ignores else set()
    if args.ignores_file is not None:
        with open(args.ignores_file, "r") as ifp:
            for line in ifp:
                stripped_line = line.strip()
                if stripped_line == "":
                    continue
                for item in glob.glob(stripped_line):
                    ignores.add(item)
    result = analyze_directory(
        directory=args.dir,
        only_extensions=args.extensions,
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

    analyzedir_help = "Analyze a directory and describe its contents"
    analyzedir_command = subparsers.add_parser(
        "analyzedir", help=analyzedir_help, description=analyzedir_help
    )
    analyzedir_command.add_argument(
        "-d", "--dir", required=True, help="Directory to analyze"
    )
    analyzedir_command.add_argument(
        "--extensions", nargs="*", help="File extensions you care about"
    )
    analyzedir_command.add_argument(
        "--ignores", nargs="*", help="Files and directories to ignore"
    )
    analyzedir_command.add_argument("--ignores-file", help="File to read ignores from")
    analyzedir_command.add_argument(
        "-s",
        "--symlinks",
        action="store_true",
        help="Set this flag to follow symbol links to directories",
    )
    analyzedir_command.set_defaults(func=handle_analyzedir)

    return parser


def main() -> None:
    parser = generate_argument_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
