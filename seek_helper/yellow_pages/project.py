import requests
from http_helper import HttpHelper
from assets.data_file import DataFile


class Project(HttpHelper):

    def __init__(self, token: str, base_url: str, output_path: str):
        super().__init__(token=token, url=f'{base_url}/projects')
        self.token = token
        self.base_url = base_url
        self.output_path = output_path

    def download_data_files(self, id: str, limit: int = 10) -> None:
        r = requests.get(f'{self.url}/{id}', headers=self.headers)
        r.raise_for_status()
        response = r.json()

        data_files = response['data']['relationships']['data_files']['data']
        ids = [data_file['id'] for data_file in data_files]

        df = DataFile(self.token, self.base_url, self.output_path)
        for id in ids[:limit]:
            df.download(id)
