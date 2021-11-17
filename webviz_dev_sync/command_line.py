import argparse

from .webviz_dev_sync import start_webviz_dev_sync


def main() -> None:

    parser = argparse.ArgumentParser(prog=("Start the Webviz development syncer tool"))

    subparsers = parser.add_subparsers(
        metavar="SUBCOMMAND",
        help="Below are the available subcommands listed. "
        "Type e.g. 'webviz-dev-sync start --help' "
        "to get help on one particular "
        "subcommand.",
    )

    parser_build = subparsers.add_parser(
        "start", help="Start the Webviz development syncer tool"
    )

    parser_build.set_defaults(func=start_webviz_dev_sync)

    args = parser.parse_args()

    args.func(args)
