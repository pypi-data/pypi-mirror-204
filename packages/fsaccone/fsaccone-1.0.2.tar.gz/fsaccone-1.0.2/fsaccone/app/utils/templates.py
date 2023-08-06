from .fetch import fetch_json
from typing import List


def get_templates() -> List[str]:
    repos = fetch_json("https://api.github.com/users/fsaccone/repos")

    repo_names: List[str] = list(
        map(
            lambda r: r["name"],
            repos,
        )
    )

    template_repo_names: List[str] = list(
        filter(
            lambda n: n.startswith("cli-template-"),
            repo_names,
        )
    )

    templates = list(
        map(
            lambda t: t.replace("cli-template-", "", 1),
            template_repo_names,
        )
    )

    return templates
