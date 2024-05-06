from seek_helper.http_helper import HttpHelper


class Programme(HttpHelper):

    def __init__(self, token: str, base_url: str):
        super().__init__(token=token, url=f'{base_url}/programmes')
