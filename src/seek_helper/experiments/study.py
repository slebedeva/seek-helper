from seek_helper.http_helper import HttpHelper


class Study(HttpHelper):

    def __init__(self, token: str, base_url: str):
        super().__init__(token=token, url=f'{base_url}/studies')
