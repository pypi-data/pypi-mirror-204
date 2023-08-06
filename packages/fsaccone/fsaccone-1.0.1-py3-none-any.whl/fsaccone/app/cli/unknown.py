from ..utils import logger
from typing import List


def unknown_template_message(template: str, templates: List[str]) -> None:
    logger.log_information(f'Unkown template "{template}"')
    logger.log_information("\nHere's a list of the templates:")
    logger.log_list(templates)
