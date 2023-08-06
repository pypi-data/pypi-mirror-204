import argparse
import logging
import os
import sys

from .commands import download, generate


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Subcommand Download
    parser_download = subparsers.add_parser("download", description="Download stock information from KABU+")
    parser_download.add_argument("dir_path", type=str)
    parser_download.add_argument("--limit", type=int)
    parser_download.add_argument("--config", type=str)
    parser_download.add_argument("--only_brand", action="store_true")
    parser_download.add_argument("--only_stock", action="store_true")
    parser_download.add_argument("--only_statements", action="store_true")
    parser_download.add_argument("--only_yahoo", action="store_true")
    parser_download.add_argument("--dot_file", type=str)
    parser_download.add_argument("--username", type=str)
    parser_download.add_argument("--password", type=str)
    parser_download.set_defaults(handler=command_download)

    # Subcommand generate
    parser_preprocess = subparsers.add_parser("generate", description="Build dataset")
    parser_preprocess.add_argument("dir_path", type=str)
    parser_preprocess.add_argument("--config", type=str)
    parser_preprocess.add_argument("--all", action="store_true")
    parser_preprocess.add_argument("--only_csv", action="store_true")
    parser_preprocess.add_argument("--only_sql", action="store_true")
    parser_preprocess.set_defaults(handler=command_generate)
    return parser


def command_download(args: argparse.Namespace) -> None:
    logging.basicConfig(level=logging.INFO)
    download.run_download(args)


def command_generate(args: argparse.Namespace) -> None:
    logging.basicConfig(level=logging.INFO)
    dir_path = os.path.expanduser(args.dir_path)
    generate_all = args.all
    only_csv = args.only_csv
    only_sql = args.only_sql
    generate.run_generate(dir_path, generate_all, only_csv, only_sql)


def main() -> None:
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
