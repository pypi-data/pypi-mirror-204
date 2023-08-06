import json
from typing import List, Dict
from urllib.request import urlopen, urlretrieve


def fetch_json(url: str) -> List | Dict:
    res: List = urlopen(url)
    data = json.load(res)

    return data


def fetch_file(url: str, path: str) -> None:
    urlretrieve(url, path)
