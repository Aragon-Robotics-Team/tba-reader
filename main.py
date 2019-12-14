import tba


def gen_api():
    token = tba.read_token()
    api = tba.Api(token, debug=True, pythonanywhere=False)

    return api


TEAM = "frc840"


def main():
    api = gen_api()

    # get all events TEAM goes to in 2019

    # events =


if __name__ == "__main__":
    main()
