import pytest
import json
from unittest import mock
from seek_helper.http_helper import HttpHelper

RESPONSE = '{"data": {}}'


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
        return MockResponse(200, RESPONSE)
    monkeypatch.setattr('requests.get', mock_get)

    def mock_post(url, headers, json):
        return MockResponse(200, RESPONSE)
    monkeypatch.setattr('requests.post', mock_post)

    def mock_patch(url, headers, json):
        return MockResponse(200, RESPONSE)
    monkeypatch.setattr('requests.patch', mock_patch)

    def mock_delete(url, headers):
        return MockResponse(200, RESPONSE)
    monkeypatch.setattr('requests.delete', mock_delete)


@pytest.fixture
def http_helper():
    return HttpHelper('token', 'http://localhost:3000')


class TestHttpHelper:
    def test_get(self, http_helper):
        result = http_helper.get()

        assert result == json.loads(RESPONSE)

    def test_create(self, http_helper):
        result = http_helper.create({})

        assert result == json.loads(RESPONSE)

    def test_update(self, http_helper):
        result = http_helper.update(1, {})

        assert result == json.loads(RESPONSE)

    def test_delete(self, http_helper):
        result = http_helper.delete(1)

        assert result == json.loads(RESPONSE)
