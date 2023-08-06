from .build import build_template
from .cli.confirm import confirmation
from .cli.help import help_message
from .cli.unknown import unknown_template_message
from .utils.templates import get_templates
from .utils.logger import log_information
import os
import pkg_resources


def start_app(args) -> None:
    if args["version"]:
        print(f'v{pkg_resources.get_distribution("fsaccone").version}')
        return

    templates = get_templates()

    template = args["template"]
    directory = os.path.abspath(args["directory"]) if args["directory"] else os.getcwd()

    os.makedirs(directory, exist_ok=True)

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
