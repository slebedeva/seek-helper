import pytest
import json
from unittest import mock
from seek_helper.yellow_pages.institution import Institution

GET_RESPONSE = '{"data":[{"id":"1","type":"institutions","attributes":{"title":"Default Institution"},"links":{"self":"/institutions/1"}}],"jsonapi":{"version":"1.0"},"links":{"self":"/institutions?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","first":"/institutions?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","prev":null,"next":null,"last":"/institutions?page%5Bnumber%5D=1&page%5Bsize%5D=1000000"},"meta":{"base_url":"http://localhost:3000","api_version":"0.3"}}'
POST_RESPONSE = '{"data":{"id":"2","type":"institutions","attributes":{"discussion_links":[],"avatar":null,"title":"Institution Example","country":"Brazil","country_code":null,"city":null,"address":null,"web_page":null},"relationships":{"people":{"data":[]},"projects":{"data":[]}},"links":{"self":"/institutions/2"},"meta":{"created":"2024-05-06T14:23:53.000Z","modified":"2024-05-06T14:23:53.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"309ccf60-ede2-013c-a6cb-00155d75bb1d"}},"jsonapi":{"version":"1.0"}}'
PATCH_RESPONSE = '{"data":{"id":"2","type":"institutions","attributes":{"discussion_links":[],"avatar":null,"title":"Institution Update Example","country":null,"country_code":null,"city":null,"address":null,"web_page":null},"relationships":{"people":{"data":[]},"projects":{"data":[]}},"links":{"self":"/institutions/2"},"meta":{"created":"2024-05-06T14:23:53.000Z","modified":"2024-05-06T14:28:43.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"309ccf60-ede2-013c-a6cb-00155d75bb1d"}},"jsonapi":{"version":"1.0"}}'
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
def institution():
    return Institution('token', 'http://localhost:3000')


class TestInstitution:
    def test_get(self, institution):
        result = institution.get()

        assert result == json.loads(GET_RESPONSE)

    def test_create(self, institution):
        payload = {
            'data': {
                'type': 'institutions',
                'attributes': {
                    'title': 'Institution Example',
                    'country': 'Brazil',
                }
            }
        }

        result = institution.create(payload)

        assert result == json.loads(POST_RESPONSE)
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['title'] == payload['data']['attributes']['title']
        assert result['data']['attributes']['country'] == payload['data']['attributes']['country']

    def test_update(self, institution):
        payload = {
            'data': {
                'id': '2',
                'type': 'institutions',
                'attributes': {
                    'title': 'Institution Update Example',
                },
            }
        }

        result = institution.update(2, payload)

        assert result == json.loads(PATCH_RESPONSE)
        assert result['data']['id'] == payload['data']['id']
        assert result['data']['attributes']['title'] == payload['data']['attributes']['title']

    def test_delete(self, institution):
        result = institution.delete(1)

        assert result == json.loads(DELETE_RESPONSE)
