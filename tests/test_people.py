import pytest
import json
from unittest import mock
from seek_helper.yellow_pages.people import People

GET_RESPONSE = '{"data":[{"id":"1","type":"people","attributes":{"title":"Person Example"},"links":{"self":"/people/1"}}],"jsonapi":{"version":"1.0"},"links":{"self":"/people?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","first":"/people?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","prev":null,"next":null,"last":"/people?page%5Bnumber%5D=1&page%5Bsize%5D=1000000"},"meta":{"base_url":"http://localhost:3000","api_version":"0.3"}}'
POST_RESPONSE = '{"data":{"id":"2","type":"people","attributes":{"avatar":null,"title":"Person First Name Example Person Last Name Example","description":null,"first_name":"Person First Name Example","last_name":"Person Last Name Example","orcid":null,"mbox_sha1sum":"ebf3b367ae950754e952c7338bbd8592e71ce29f","expertise":[],"tools":[],"login":null},"relationships":{"projects":{"data":[]},"institutions":{"data":[]},"investigations":{"data":[]},"studies":{"data":[]},"assays":{"data":[]},"data_files":{"data":[]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"presentations":{"data":[]},"events":{"data":[]},"documents":{"data":[]},"workflows":{"data":[]},"collections":{"data":[]}},"links":{"self":"/people/2"},"meta":{"created":"2024-05-06T14:41:31.000Z","modified":"2024-05-06T14:41:31.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"a6f3f4e0-ede4-013c-a6cb-00155d75bb1d"}},"jsonapi":{"version":"1.0"}}'
PATCH_RESPONSE = '{"data":{"id":"2","type":"people","attributes":{"avatar":null,"title":"Person First Name Update Example Person Last Name Example","description":null,"first_name":"Person First Name Update Example","last_name":"Person Last Name Example","orcid":null,"mbox_sha1sum":"ebf3b367ae950754e952c7338bbd8592e71ce29f","expertise":[],"tools":[],"login":null},"relationships":{"projects":{"data":[]},"institutions":{"data":[]},"investigations":{"data":[]},"studies":{"data":[]},"assays":{"data":[]},"data_files":{"data":[]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"presentations":{"data":[]},"events":{"data":[]},"documents":{"data":[]},"workflows":{"data":[]},"collections":{"data":[]}},"links":{"self":"/people/2"},"meta":{"created":"2024-05-06T14:41:31.000Z","modified":"2024-05-06T14:53:45.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"a6f3f4e0-ede4-013c-a6cb-00155d75bb1d"}},"jsonapi":{"version":"1.0"}}'
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
def people():
    return People('token', 'http://localhost:3000')


class TestPeople:
    def test_get(self, people):
        result = people.get()

        assert result == json.loads(GET_RESPONSE)

    def test_create(self, people):
        payload = {
            'data': {
                'type': 'people',
                'attributes': {
                    'first_name': 'Person First Name Example',
                    'last_name': 'Person Last Name Example',
                    'email': 'email@example.com',
                },
            }
        }

        result = people.create(payload)

        assert result == json.loads(POST_RESPONSE)
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['first_name'] == payload['data']['attributes']['first_name']
        assert result['data']['attributes']['last_name'] == payload['data']['attributes']['last_name']

    def test_update(self, people):
        payload = {
            'data': {
                'id': '2',
                'type': 'people',
                'attributes': {
                    'first_name': 'Person First Name Update Example',
                },
            }
        }

        result = people.update(2, payload)

        assert result == json.loads(PATCH_RESPONSE)
        assert result['data']['id'] == payload['data']['id']
        assert result['data']['attributes']['first_name'] == payload['data']['attributes']['first_name']

    def test_delete(self, people):
        result = people.delete(1)

        assert result == json.loads(DELETE_RESPONSE)

    def get_current(self, people):
        result = people.get_current()

        assert result == json.loads(GET_RESPONSE)
