from .tba_api import Api


def read_token(file="secret.txt"):
    with open(file, "r") as f:
        token = f.read()

    token = token.strip().upper()

    return token
