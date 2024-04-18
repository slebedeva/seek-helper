import requests
from seek_helper.http_helper import HttpHelper


class DataFile(HttpHelper):

    def __init__(self, token: str, base_url: str, output_path: str):
        super().__init__(token=token, url=f'{base_url}/data_files')
        self.output_path = output_path

    def download(self, id: int) -> None:
        r = requests.get(f'{self.url}/{id}', headers=self.headers)
        r.raise_for_status()
        data_file = r.json()

        content_blobs = data_file['data']['attributes']['content_blobs']
        files = [{'filename': content_blob['original_filename'],
                  'link': content_blob['link']} for content_blob in content_blobs]

        for file in files:
            r = requests.get(f"{file['link']}/download", headers=self.headers)
            r.raise_for_status()
            with open(f"{self.output_path}/{file['filename']}", 'wb') as f:
                f.write(r.content)
