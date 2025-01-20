import mimetypes
import requests
import uuid
from seek_helper.http_helper import HttpHelper


class DataFile(HttpHelper):

    def __init__(self, token: str, base_url: str, output_path: str, input_path: str, experimental_features: bool = False):
        super().__init__(token=token, url=f'{base_url}/data_files')
        self.output_path = output_path
        self.input_path = input_path
        self.experimental_features = experimental_features

    def download(self, id: int) -> None:
        data_file = self.get(id)

        content_blobs = data_file['data']['attributes']['content_blobs']
        files = [{'filename': content_blob['original_filename'],
                  'link': content_blob['link']} for content_blob in content_blobs]

        for file in files:
            r = requests.get(f"{file['link']}/download", headers=self.headers)
            r.raise_for_status()
            with open(f"{self.output_path}/{id}_{file['filename']}", 'wb') as f:
                f.write(r.content)

    def upload_to_s3(self, bucket: str, filename: str, project_id: int) -> None:
        if not self.experimental_features:
            print('This operation is not available. Please enable experimental features to use it.')
            return

        key = str(uuid.uuid4())

        r = requests.get(f'{self.url}/s3_presigned_url?method=put&bucket={bucket}&key={key}', headers=self.headers)
        r.raise_for_status()
        url = r.json().get('url')

        with open(f"{self.input_path}/{filename}", 'rb') as f:
            r = requests.put(url, data=f)
            r.raise_for_status()

        payload = {
            'data': {
                'type': 'data_files',
                'attributes': {
                    'title': filename,
                        'content_blobs': [
                            {
                                'original_filename': filename,
                                'content_type': mimetypes.guess_type(filename)[0],
                                's3_key': key
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
                }
            }
        }
        self.create(payload)
