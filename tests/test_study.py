import pytest
import json
from unittest import mock
from seek_helper.experiments.study import Study

GET_RESPONSE = '{"data":[{"id":"1","type":"studies","attributes":{"title":"Study Example"},"links":{"self":"/studies/1"}}],"jsonapi":{"version":"1.0"},"links":{"self":"/studies?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","first":"/studies?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","prev":null,"next":null,"last":"/studies?page%5Bnumber%5D=1&page%5Bsize%5D=1000000"},"meta":{"base_url":"http://localhost:3000","api_version":"0.3"}}'
POST_RESPONSE = '{"data":{"id":"2","type":"studies","attributes":{"policy":{"access":"no_access","permissions":[]},"discussion_links":[],"snapshots":[],"title":"Study Example","description":"This is an example of study creation","experimentalists":null,"other_creators":null,"position":null,"creators":[]},"relationships":{"creators":{"data":[]},"submitter":{"data":[{"id":"1","type":"people"}]},"people":{"data":[{"id":"1","type":"people"}]},"projects":{"data":[{"id":"1","type":"projects"}]},"investigation":{"data":{"id":"1","type":"investigations"}},"assays":{"data":[]},"data_files":{"data":[]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"documents":{"data":[]}},"links":{"self":"/studies/2"},"meta":{"created":"2024-05-02T09:29:34.000Z","modified":"2024-05-02T09:29:34.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"6983a2f0-ea94-013c-5750-00155d0fd7d9"}},"jsonapi":{"version":"1.0"}}'
PATCH_RESPONSE = '{"data":{"id":"1","type":"studies","attributes":{"policy":{"access":"no_access","permissions":[{"resource":{"id":"1","type":"projects"},"access":"download"}]},"discussion_links":[],"snapshots":[],"title":"Study Example","description":"This is an example of study update","experimentalists":null,"other_creators":"","position":null,"creators":[]},"relationships":{"creators":{"data":[{"id":"1","type":"people"}]},"submitter":{"data":[{"id":"1","type":"people"}]},"people":{"data":[{"id":"1","type":"people"}]},"projects":{"data":[{"id":"1","type":"projects"}]},"investigation":{"data":{"id":"1","type":"investigations"}},"assays":{"data":[{"id":"1","type":"assays"},{"id":"2","type":"assays"},{"id":"3","type":"assays"}]},"data_files":{"data":[{"id":"1","type":"data_files"}]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"documents":{"data":[]}},"links":{"self":"/studies/1"},"meta":{"created":"2024-04-03T15:24:00.000Z","modified":"2024-05-02T09:32:02.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"1e9700e0-d3fc-013c-780a-00155ddef5bd"}},"jsonapi":{"version":"1.0"}}'
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
def study():
    return Study('token', 'http://localhost:3000')


class TestStudy:
    def test_get(self, study):
        result = study.get()

        assert result == json.loads(GET_RESPONSE)

    def test_create(self, study):
        payload = {
            'data': {
                'type': 'studies',
                'attributes': {
                    'title': 'Study Example',
                    'description': 'This is an example of study creation',
                },
                'relationships': {
                    'investigation': {
                        'data': {
                            'id': '1',
                            'type': 'investigations'
                        }
                    },
                }
            }
        }

        result = study.create(payload)

        assert result == json.loads(POST_RESPONSE)
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['title'] == payload['data']['attributes']['title']
        assert result['data']['attributes']['description'] == payload['data']['attributes']['description']
        assert result['data']['relationships']['investigation']['data'][
            'id'] == payload['data']['relationships']['investigation']['data']['id']
        assert result['data']['relationships']['investigation']['data'][
            'type'] == payload['data']['relationships']['investigation']['data']['type']

    def test_update(self, study):
        payload = {
            'data': {
                'id': '1',
                'type': 'studies',
                'attributes': {
                    'description': 'This is an example of study update',
                },
            }
        }

        result = study.update(1, payload)

        assert result == json.loads(PATCH_RESPONSE)
        assert result['data']['id'] == payload['data']['id']
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['description'] == payload['data']['attributes']['description']

    def test_delete(self, study):
        result = study.delete(1)

        assert result == json.loads(DELETE_RESPONSE)
