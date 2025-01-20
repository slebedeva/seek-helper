import mimetypes
import os
import requests
from seek_helper.http_helper import HttpHelper
from seek_helper.assets.data_file import DataFile


class Assay(HttpHelper):

    def __init__(self, token: str, base_url: str, input_path: str, data_file: DataFile):
        super().__init__(token=token, url=f'{base_url}/assays')
        self.input_path = input_path
        self.data_file = data_file

    def download_data_files(self, id: int, limit: int = 10) -> None:
        assay = self.get(id)

        data_files = assay['data']['relationships']['data_files']['data']
        ids = [data_file['id'] for data_file in data_files]

        for id in ids[:limit]:
            self.data_file.download(id)

    def upload_data_files(self, assay_id: int, project_id: int, limit: int = 10) -> None:
        files = os.listdir(self.input_path)

        for file in files[:limit]:
            payload = {
                'data': {
                    'type': 'data_files',
                    'attributes': {
                        'title': file,
                            'content_blobs': [
                                {
                                    'original_filename': file,
                                    'content_type': mimetypes.guess_type(file)[0]
                                }
                            ],
                    },
                    'relationships': {
                        'projects': {
                            'data': [
                                {
                                    'id': project_id,
                                    'type': 'projects'
                                }
                            ]
                        },
                        'assays': {
                            'data': [
                                {
                                    'id': assay_id,
                                    'type': 'assays'
                                }
                            ]
                        },
                    }
                }
            }
            data_file = self.data_file.create(payload)

            content_blob_link = data_file['data']['attributes']['content_blobs'][0]['link']
            f = {'file': open(f'{self.input_path}/{file}', 'rb')}

            r = requests.put(content_blob_link, headers=self.headers, files=f)
            r.raise_for_status()
