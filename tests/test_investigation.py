import pytest
import json
from unittest import mock
from seek_helper.experiments.investigation import Investigation

GET_RESPONSE = '{"data":[{"id":"1","type":"investigations","attributes":{"title":"Investigation Example"},"links":{"self":"/investigations/1"}},{"id":"1","type":"investigations","attributes":{"title":"Investigation Example 1"},"links":{"self":"/investigations/1"}}],"jsonapi":{"version":"1.0"},"links":{"self":"/investigations?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","first":"/investigations?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","prev":null,"next":null,"last":"/investigations?page%5Bnumber%5D=1&page%5Bsize%5D=1000000"},"meta":{"base_url":"http://localhost:3000","api_version":"0.3"}}'
POST_RESPONSE = '{"data":{"id":"2","type":"investigations","attributes":{"policy":{"access":"no_access","permissions":[]},"discussion_links":[],"snapshots":[],"title":"Investigation Example","description":"This is an example of investigation creation","other_creators":null,"position":null,"creators":[]},"relationships":{"creators":{"data":[]},"submitter":{"data":[{"id":"1","type":"people"}]},"people":{"data":[{"id":"1","type":"people"}]},"projects":{"data":[{"id":"1","type":"projects"}]},"studies":{"data":[]},"assays":{"data":[]},"data_files":{"data":[]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"documents":{"data":[]}},"links":{"self":"/investigations/2"},"meta":{"created":"2024-05-02T09:39:46.000Z","modified":"2024-05-02T09:39:46.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"d5f82390-ea95-013c-5750-00155d0fd7d9"}},"jsonapi":{"version":"1.0"}}'
PATCH_RESPONSE = '{"data":{"id":"2","type":"investigations","attributes":{"policy":{"access":"no_access","permissions":[{"resource":{"id":"1","type":"projects"},"access":"download"}]},"discussion_links":[],"extended_attributes":{"extended_metadata_type_id":"1","attribute_map":{"id":"123","submission_date":"","license":"","miappe_version":"1"}},"snapshots":[],"title":"Investigation Example","description":"This is an example of investigation update","other_creators":"","position":null,"creators":[]},"relationships":{"creators":{"data":[{"id":"1","type":"people"}]},"submitter":{"data":[{"id":"1","type":"people"}]},"people":{"data":[{"id":"1","type":"people"}]},"projects":{"data":[{"id":"1","type":"projects"}]},"studies":{"data":[{"id":"1","type":"studies"},{"id":"2","type":"studies"}]},"assays":{"data":[{"id":"1","type":"assays"},{"id":"2","type":"assays"},{"id":"3","type":"assays"}]},"data_files":{"data":[{"id":"1","type":"data_files"}]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"documents":{"data":[]}},"links":{"self":"/investigations/2"},"meta":{"created":"2024-03-26T14:26:05.000Z","modified":"2024-05-02T09:44:54.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"b471a490-cdaa-013c-c444-00155dee8a98"}},"jsonapi":{"version":"1.0"}}'
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
def investigation():
    return Investigation('token', 'http://localhost:3000')


class TestInvestigation:
    def test_get(self, investigation):
        result = investigation.get()

        assert result == json.loads(GET_RESPONSE)

    def test_create(self, investigation):
        payload = {
            'data': {
                'type': 'investigations',
                'attributes': {
                    'title': 'Investigation Example',
                    'description': 'This is an example of investigation creation',
                },
                'relationships': {
                    'projects': {
                        'data': [
                            {
                                'type': 'projects',
                                'id': '1',
                            },
                        ]
                    },
                }
            }
        }

        result = investigation.create(payload)

        assert result == json.loads(POST_RESPONSE)
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['title'] == payload['data']['attributes']['title']
        assert result['data']['attributes']['description'] == payload['data']['attributes']['description']
        assert result['data']['relationships']['projects']['data'][0]['id'] == payload['data']['relationships']['projects']['data'][0]['id']
        assert result['data']['relationships']['projects']['data'][0]['type'] == payload['data']['relationships']['projects']['data'][0]['type']

    def test_update(self, investigation):
        payload = {
            'data': {
                'id': '2',
                'type': 'investigations',
                'attributes': {
                    'description': 'This is an example of investigation update',
                },
            }
        }

        result = investigation.update(2, payload)

        assert result == json.loads(PATCH_RESPONSE)
        assert result['data']['id'] == payload['data']['id']
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['description'] == payload['data']['attributes']['description']

    def test_delete(self, investigation):
        result = investigation.delete(1)

        assert result == json.loads(DELETE_RESPONSE)
