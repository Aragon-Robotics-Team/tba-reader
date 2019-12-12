import tba

def main():
    token = tba.read_token()
    api = Api(token, debug=True)

if __name__ == "__main__":
    main()
