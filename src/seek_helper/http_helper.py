import requests


class HttpHelper():
    def __init__(self, token: str, url: str):
        self.headers = {
            'Accept': 'application/vnd.api+json',
            'Accept-Charset': 'ISO-8859-1',
            'Authorization': f'Token {token}'
        }
        self.url = url

    def get(self, id: int = None) -> dict:
        url = f'{self.url}/{id}' if id else self.url
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return r.json()

    def create(self, data: dict) -> dict:
        r = requests.post(self.url, headers=self.headers, json=data)
        r.raise_for_status()
        return r.json()

    def update(self, id: int, data: dict) -> dict:
        r = requests.patch(f'{self.url}/{id}', headers=self.headers, json=data)
        r.raise_for_status()
        return r.json()

    def delete(self, id: int) -> dict:
        r = requests.delete(f'{self.url}/{id}', headers=self.headers)
        r.raise_for_status()
        return r.json()
