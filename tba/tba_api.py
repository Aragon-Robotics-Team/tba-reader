import tbaapiv3client

__all__ = ("Api",)


class ApiClientWrapper(tbaapiv3client.ApiClient):
    def __init__(self, config, async_req=False):
        super().__init__(config)
        self.async_req = async_req

    def call_api(self, *args, **kwargs):
        kwargs["async_req"] = self.async_req
        return super().call_api(*args, **kwargs)


class Api:
    def __init__(self, token, *, debug=False, async_req=False, pythonanywhere=False):
        self.token = str(token)
        self.debug = bool(debug)
        self.async_req = bool(async_req)
        self.pythonanywhere = bool(pythonanywhere)

        self.create_api()
        self.create_child_apis()

    def create_api(self):
        config = tbaapiv3client.Configuration()

        config.api_key["X-TBA-Auth-Key"] = self.token
        config.debug = self.debug
        if self.pythonanywhere:
            config.proxy = "http://proxy.server:3128"

        self.api = ApiClientWrapper(config, self.async_req)

    def create_child_apis(self):
        self.event = tbaapiv3client.EventApi(self.api)
        self.team = tbaapiv3client.TeamApi(self.api)
        self.tba = tbaapiv3client.TBAApi(self.api)
        self.match = tbaapiv3client.MatchApi(self.api)
        self.list = tbaapiv3client.ListApi(self.api)
