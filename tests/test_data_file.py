import pytest
import json
from unittest import mock
from seek_helper.assets.data_file import DataFile

GET_RESPONSE = '{"data":[{"id":"1","type":"data_files","attributes":{"title":"Data File Example 1"},"links":{"self":"/data_files/1"}},{"id":"3","type":"data_files","attributes":{"title":"Data File Example 3"},"links":{"self":"/data_files/3"}},{"id":"2","type":"data_files","attributes":{"title":"Data File Example 2"},"links":{"self":"/data_files/2"}}],"jsonapi":{"version":"1.0"},"links":{"self":"/data_files?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","first":"/data_files?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","prev":null,"next":null,"last":"/data_files?page%5Bnumber%5D=1&page%5Bsize%5D=1000000"},"meta":{"base_url":"http://localhost:3000","api_version":"0.3"}}'
POST_RESPONSE = '{"data":{"id":"2","type":"data_files","attributes":{"policy":{"access":"no_access","permissions":[]},"discussion_links":[],"title":"Data File Example","license":null,"description":null,"latest_version":1,"tags":[],"versions":[{"version":1,"revision_comments":null,"url":"http://localhost:3000/data_files/2?version=1","doi":null}],"version":1,"revision_comments":null,"created_at":"2024-05-02T09:57:36.000Z","updated_at":"2024-05-02T09:57:36.000Z","doi":null,"content_blobs":[{"original_filename":"file.jpg","url":null,"md5sum":null,"sha1sum":null,"content_type":"image/jpeg","link":"http://localhost:3000/data_files/2/content_blobs/102","size":null}],"creators":[],"other_creators":null,"data_type_annotations":[],"data_format_annotations":[]},"relationships":{"creators":{"data":[]},"submitter":{"data":[{"id":"1","type":"people"}]},"people":{"data":[{"id":"1","type":"people"}]},"projects":{"data":[{"id":"1","type":"projects"}]},"investigations":{"data":[]},"studies":{"data":[]},"assays":{"data":[]},"publications":{"data":[]},"events":{"data":[]},"workflows":{"data":[]},"placeholder":{"data":null},"file_template":{"data":null}},"links":{"self":"/data_files/2?version=1"},"meta":{"created":"2024-05-02T09:57:36.000Z","modified":"2024-05-02T09:57:36.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"53b1f520-ea98-013c-5750-00155d0fd7d9"}},"jsonapi":{"version":"1.0"}}'
PATCH_RESPONSE = '{"data":{"id":"2","type":"data_files","attributes":{"policy":{"access":"no_access","permissions":[{"resource":{"id":"1","type":"projects"},"access":"download"}]},"discussion_links":[],"title":"Testfile","license":"CC-BY-4.0","description":"This is an example of data file update","latest_version":2,"tags":[],"versions":[{"version":1,"revision_comments":null,"url":"http://localhost:3000/data_files/1?version=1","doi":null},{"version":2,"revision_comments":null,"url":"http://localhost:3000/data_files/1?version=2","doi":null}],"version":2,"revision_comments":null,"created_at":"2024-04-17T10:35:27.000Z","updated_at":"2024-05-02T10:02:43.000Z","doi":null,"content_blobs":[{"original_filename":"plant4.webp","url":null,"md5sum":"b5f84d79502eb95169d7ecf357cccd0c","sha1sum":"649db18c1a18e2f5ce8e9a90a3ce202ef0639443","content_type":"image/webp","link":"http://localhost:3000/data_files/1/content_blobs/50","size":560896}],"creators":[],"other_creators":"","data_type_annotations":[],"data_format_annotations":[]},"relationships":{"creators":{"data":[{"id":"1","type":"people"}]},"submitter":{"data":[{"id":"1","type":"people"}]},"people":{"data":[{"id":"1","type":"people"}]},"projects":{"data":[{"id":"1","type":"projects"}]},"investigations":{"data":[{"id":"1","type":"investigations"}]},"studies":{"data":[{"id":"1","type":"studies"}]},"assays":{"data":[{"id":"1","type":"assays"},{"id":"2","type":"assays"}]},"publications":{"data":[]},"events":{"data":[]},"workflows":{"data":[]},"placeholder":{"data":null},"file_template":{"data":null}},"links":{"self":"/data_files/2?version=1"},"meta":{"created":"2024-04-03T15:26:49.000Z","modified":"2024-05-02T10:02:43.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"835f1070-d3fc-013c-780a-00155ddef5bd"}},"jsonapi":{"version":"1.0"}}'
DELETE_RESPONSE = '{"status": "ok"}'


class MockResponse:
    def __init__(self, status_code: int, text: str):
        self.status_code = status_code
        self.text = text
        self.raise_for_status = mock.Mock()

    def json(self):
        return json.loads(self.text)


@pytest.fixture(autouse=True)
def mock_requests(monkeypatch):

    def mock_get(url, headers):
        return MockResponse(200, GET_RESPONSE)
    monkeypatch.setattr('requests.get', mock_get)

    def mock_post(url, headers, json):
        return MockResponse(200, POST_RESPONSE)
    monkeypatch.setattr('requests.post', mock_post)

    def mock_patch(url, headers, json):
        return MockResponse(200, PATCH_RESPONSE)
    monkeypatch.setattr('requests.patch', mock_patch)

    def mock_delete(url, headers):
        return MockResponse(200, DELETE_RESPONSE)
    monkeypatch.setattr('requests.delete', mock_delete)


@pytest.fixture
def data_file():
    return DataFile('token', 'http://localhost:3000', 'output_path')


class TestDataFile:
    def test_get(self, data_file):
        result = data_file.get()

        assert result == json.loads(GET_RESPONSE)

    def test_create(self, data_file):
        payload = {
            'data': {
                'type': 'data_files',
                'attributes': {
                    'title': 'Data File Example',
                    'content_blobs': [
                        {
                            'original_filename': 'file.jpg',
                            'content_type': 'image/jpeg',
                        }
                    ],
                },
                'relationships': {
                    'projects': {
                        'data': [
                            {
                                'id': '1',
                                'type': 'projects',
                            }
                        ]
                    },
                }
            }
        }

        result = data_file.create(payload)

        assert result == json.loads(POST_RESPONSE)
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['title'] == payload['data']['attributes']['title']
        assert result['data']['attributes']['content_blobs'][0]['original_filename'] == payload[
            'data']['attributes']['content_blobs'][0]['original_filename']
        assert result['data']['attributes']['content_blobs'][0]['content_type'] == payload['data']['attributes']['content_blobs'][0]['content_type']
        assert result['data']['relationships']['projects']['data'][0]['id'] == payload['data']['relationships']['projects']['data'][0]['id']
        assert result['data']['relationships']['projects']['data'][0]['type'] == payload['data']['relationships']['projects']['data'][0]['type']

    def test_update(self, data_file):
        payload = {
            'data': {
                'id': '2',
                'type': 'data_files',
                'attributes': {
                    'description': 'This is an example of data file update',
                },
            }
        }

        result = data_file.update(2, payload)

        assert result == json.loads(PATCH_RESPONSE)
        assert result['data']['id'] == payload['data']['id']
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['description'] == payload['data']['attributes']['description']

    def test_delete(self, data_file):
        result = data_file.delete(1)

        assert result == json.loads(DELETE_RESPONSE)

    # TODO: test_download
