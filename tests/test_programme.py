import pytest
import json
from unittest import mock
from seek_helper.yellow_pages.programme import Programme

GET_RESPONSE = '{"data":[{"id":"1","type":"programmes","attributes":{"title":"Programme Test"},"links":{"self":"/programmes/1"}}],"jsonapi":{"version":"1.0"},"links":{"self":"/programmes?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","first":"/programmes?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","prev":null,"next":null,"last":"/programmes?page%5Bnumber%5D=1&page%5Bsize%5D=1000000"},"meta":{"base_url":"http://localhost:3000","api_version":"0.3"}}'
POST_RESPONSE = '{"data":{"id":"2","type":"programmes","attributes":{"discussion_links":[],"avatar":null,"title":"Programme Example","description":null,"web_page":null,"funding_details":null,"funding_codes":[]},"relationships":{"administrators":{"data":[]},"people":{"data":[]},"projects":{"data":[]},"institutions":{"data":[]},"investigations":{"data":[]},"studies":{"data":[]},"assays":{"data":[]},"data_files":{"data":[]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"presentations":{"data":[]},"events":{"data":[]},"documents":{"data":[]},"workflows":{"data":[]},"collections":{"data":[]}},"links":{"self":"/programmes/2"},"meta":{"created":"2024-05-06T15:25:27.000Z","modified":"2024-05-06T15:25:27.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"c9ff7c60-edea-013c-a6cc-00155d75bb1d"}},"jsonapi":{"version":"1.0"}}'
PATCH_RESPONSE = '{"data":{"id":"2","type":"programmes","attributes":{"discussion_links":[],"avatar":null,"title":"Programme Update Example","description":null,"web_page":null,"funding_details":null,"funding_codes":[]},"relationships":{"administrators":{"data":[]},"people":{"data":[]},"projects":{"data":[]},"institutions":{"data":[]},"investigations":{"data":[]},"studies":{"data":[]},"assays":{"data":[]},"data_files":{"data":[]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"presentations":{"data":[]},"events":{"data":[]},"documents":{"data":[]},"workflows":{"data":[]},"collections":{"data":[]}},"links":{"self":"/programmes/2"},"meta":{"created":"2024-05-06T15:25:27.000Z","modified":"2024-05-06T15:28:41.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"c9ff7c60-edea-013c-a6cc-00155d75bb1d"}},"jsonapi":{"version":"1.0"}}'
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
def programme():
    return Programme('token', 'http://localhost:3000')


class TestProgramme:
    def test_get(self, programme):
        result = programme.get()

        assert result == json.loads(GET_RESPONSE)

    def test_create(self, programme):
        payload = {
            'data': {
                'type': 'programmes',
                'attributes': {
                    'title': 'Programme Example',
                },
            }
        }

        result = programme.create(payload)

        assert result == json.loads(POST_RESPONSE)
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['title'] == payload['data']['attributes']['title']

    def test_update(self, programme):
        payload = {
            'data': {
                'id': '2',
                'type': 'programmes',
                'attributes': {
                        'title': 'Programme Update Example',
                },
            }
        }

        result = programme.update(2, payload)

        assert result == json.loads(PATCH_RESPONSE)
        assert result['data']['id'] == payload['data']['id']
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['title'] == payload['data']['attributes']['title']

    def test_delete(self, programme):
        result = programme.delete(1)

        assert result == json.loads(DELETE_RESPONSE)
