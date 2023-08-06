import argparse
import sys
from typing import Dict


def _parse_args() -> argparse.Namespace:
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument(
        "--directory",
        "--dir",
        "-d",
        action="store",
        default=[None],
        nargs=1,
        type=str,
    )
    args_parser.add_argument(
        "--template",
        "-t",
        action="store",
        default=[None],
        nargs=1,
        type=str,
    )
    args_parser.add_argument(
        "-y",
        action="store_true",
        default=False,
    )

    args, unknown = args_parser.parse_known_args(sys.argv[1:])
    return args


def get_none_or_normalized_string(string: str | None) -> str | None:
    return string.lower().strip() if type(string) == str else None


def get_args() -> Dict:
    args = _parse_args()

    directory = get_none_or_normalized_string(args.directory[0])

    template = get_none_or_normalized_string(args.template[0])

    y: bool = args.y

    return {
        "directory": directory,
        "template": template,
        "y": y,
    }
