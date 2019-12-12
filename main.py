import tba

def main():
    token = tba.read_token()
    api = tba.Api(token, debug=True, pythonanywhere=True)

    return api

if __name__ == "__main__":
    main()
