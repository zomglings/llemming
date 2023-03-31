import argparse

from .analyze_directory import analyze_directory
from .version import VERSION


def handle_analyzedir(args: argparse.Namespace) -> None:
    analyze_directory(directory=args.dir, symlinks=args.symlinks)


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
