import requests
from seek_helper.http_helper import HttpHelper


class People(HttpHelper):

    def __init__(self, token: str, base_url: str):
        super().__init__(token=token, url=f'{base_url}/people')

    def get_current(self) -> None:
        r = requests.get(f'{self.url}/current', headers=self.headers)
        r.raise_for_status()
        return r.json()
