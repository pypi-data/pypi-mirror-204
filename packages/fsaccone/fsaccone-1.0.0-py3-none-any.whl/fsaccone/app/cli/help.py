from ..utils import logger
from typing import List


def help_message(templates: List[str]) -> None:
    logger.log_information(
        'To build a project template, run "fsaccone --template <TEMPLATE>"'
    )
    logger.log_information("\nHere's a list of the templates:")
    logger.log_list(templates)
