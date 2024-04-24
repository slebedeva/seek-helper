import os
import mimetypes
import requests
from seek_helper.http_helper import HttpHelper
from seek_helper.assets.data_file import DataFile


class Project(HttpHelper):

    def __init__(self, token: str, base_url: str, output_path: str, input_path: str, data_file: DataFile):
        super().__init__(token=token, url=f'{base_url}/projects')
        self.token = token
        self.base_url = base_url
        self.output_path = output_path
        self.input_path = input_path
        self.data_file = data_file

    def download_data_files(self, id: str, limit: int = 10) -> None:
        project = self.get(id)

        data_files = project['data']['relationships']['data_files']['data']
        ids = [data_file['id'] for data_file in data_files]

        for id in ids[:limit]:
            self.data_file.download(id)

    def upload_data_files(self, id: str, limit: int = 10) -> None:
        files = os.listdir(self.input_path)

        for file in files[:limit]:
            mime_type = mimetypes.guess_type(file)[0]

            payload = {
                "data": {
                    "type": "data_files",
                    "attributes": {
                        "title": file,
                            "content_blobs": [
                                {
                                    "original_filename": file,
                                    "content_type": mime_type
                                }
                            ],
                    },
                    "relationships": {
                        "projects": {
                            "data": [
                                {
                                    "id": id,
                                    "type": "projects"
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
