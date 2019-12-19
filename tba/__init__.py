import tbaapiv3client

from .tba_api import Api


def read_token(file="secret.txt"):
    with open(file, "r") as f:
        token = f.read()

    token = token.strip()

    return token


MATCH_MAPPING = {
    "qm": "Qualification",
    "ef": "Eighth-Final",
    "qf": "Quarter-Final",
    "sf": "Semi-Final",
    "f": "Final",
}

MATCH_ORDER = ("qm", "ef", "qf", "sf", "f")
