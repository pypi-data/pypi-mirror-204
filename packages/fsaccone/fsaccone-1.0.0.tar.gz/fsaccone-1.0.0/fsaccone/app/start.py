from .build import build_template
from .cli.confirm import confirmation
from .cli.help import help_message
from .cli.unknown import unknown_template_message
from .utils.templates import get_templates
import os


def start_app(args) -> None:
    templates = get_templates()

    template = args["template"]
    directory = os.path.abspath(args["directory"]) if args["directory"] else os.getcwd()

    if not template:
        help_message(templates)
        return

    if not template in templates:
        unknown_template_message(template, templates)
        return

    confirmed = True if args["y"] else confirmation(directory)

    if not confirmed:
        return

    build_template(template, directory)
