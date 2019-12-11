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
    def __init__(self, token, debug=False, async_req=False):
        self.token = token
        self.debug = debug
        self.async_req = async_req

        self.create_api()
        self.create_child_apis()

    def create_api(self):
        config = tbaapiv3client.Configuration()

        config.api_key["X-TBA-Auth-Key"] = self.token
        config.debug = self.debug

        self.api = ApiClientWrapper(config, self.async_req)

    def create_child_apis(self):
        self.event = tbaapiv3client.EventApi(self.api)
        self.team = tbaapiv3client.TeamApi(self.api)
        self.tba = tbaapiv3client.TBAApi(self.api)
