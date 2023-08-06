from rich.console import Console
from typing import List

console = Console(color_system="standard")


def log_status(*text: List[str], newline=True) -> None:
    console.print(
        *text,
        style="cyan",
        end="\n" if newline else "",
    )


def log_important(*text: List[str], newline=True) -> None:
    console.print(
        *text,
        style="bold red",
        end="\n" if newline else "",
    )


def log_information(*text: List[str], newline=True) -> None:
    console.print(
        *text,
        style="italic bright_black",
        end="\n" if newline else "",
    )


def log_list(list: List[str], newline=True) -> None:
    for element in list:
        console.print(
            "  - ",
            style="bright_black",
            end="",
        )
        console.print(
            element,
            style="green",
            end="\n",
        )
