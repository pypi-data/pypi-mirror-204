from ..utils import logger


def _get_confirmation_input() -> bool:
    logger.log_important("(y/n) ", newline=False)
    confirmation = input().lower().strip()

    if not (confirmation == "y" or confirmation == "n"):
        return _get_confirmation_input()

    return True if confirmation == "y" else False


def confirmation(dir: str) -> bool:
    logger.log_information(
        "Are you sure you want to continue?",
        newline=False,
    )
    logger.log_important(f' All of the files in "{dir}" will be deleted.')

    return _get_confirmation_input()
