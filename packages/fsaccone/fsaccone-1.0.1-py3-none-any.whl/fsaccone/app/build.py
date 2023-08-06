from .utils.fetch import fetch_file
from .utils.logger import log_status, log_important
import os
import shutil
import sys
from zipfile import ZipFile


def clear_directory(dir: str) -> None:
    for child in os.listdir(dir):
        try:
            if os.path.isfile(child):
                os.unlink(child)
            elif os.path.isdir(child):
                shutil.rmtree(child)
        except Exception as e:
            log_important(f'Failed to delete "{child}". Reason: "{e}"')
            sys.exit(1)


def get_template_dir(root_dir: str) -> str:
    for child in os.listdir(root_dir):
        if child.startswith("fsaccone-cli-template-"):
            return child


def move_all_files(from_dir: str, to_dir: str) -> None:
    for child in os.listdir(from_dir):
        shutil.move(os.path.abspath(os.path.join(from_dir, child)), to_dir)


def build_template(template: str, dir: str) -> None:
    log_status("Deleting all the content in the directory...")
    clear_directory(dir)

    log_status("Downloading the template...")
    zip_url = f"https://github.com/fsaccone/cli-template-{template}/zipball/main"
    archive_path = os.path.abspath(os.path.join(dir, "template.zip"))
    fetch_file(zip_url, archive_path)

    log_status("Unzipping the archive...")
    zip_reference = ZipFile(archive_path, mode="r")
    zip_reference.extractall(dir)
    zip_reference.close()
    try:
        os.unlink(archive_path)
    except Exception as e:
        log_important(f'Failed to delete the archive. Reason: "{e}"')
        sys.exit(1)

    # Moving all the files in the extracted directory to the root directory.
    log_status("Building the template...")
    template_dir = get_template_dir(dir)
    move_all_files(template_dir, dir)
    try:
        shutil.rmtree(template_dir)
    except Exception as e:
        log_important(f'Failed to delete the unarchived directory. Reason: "{e}"')

    log_status("The template was built successfully.")
