import pytest
import json
from unittest import mock
from seek_helper.http_helper import HttpHelper

RESPONSE = '{"data": {}}'


class MockResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text
        self.raise_for_status = mock.Mock()

    def json(self):
        return json.loads(self.text)


@pytest.fixture
def mock_requests_get(monkeypatch):

    def mock_get(url, headers):
        return MockResponse(200, RESPONSE)
    monkeypatch.setattr('requests.get', mock_get)


@pytest.fixture
def mock_requests_post(monkeypatch):

    def mock_post(url, headers, json):
        return MockResponse(200, RESPONSE)
    monkeypatch.setattr('requests.post', mock_post)


@pytest.fixture
def mock_requests_patch(monkeypatch):

    def mock_patch(url, headers, json):
        return MockResponse(200, RESPONSE)
    monkeypatch.setattr('requests.patch', mock_patch)


@pytest.fixture
def mock_requests_delete(monkeypatch):

    def mock_delete(url, headers):
        return MockResponse(200, RESPONSE)
    monkeypatch.setattr('requests.delete', mock_delete)


def test_get(mock_requests_get):
    token = 'token'
    url = 'http://localhost:3000'
    http_helper = HttpHelper(token, url)

    result = http_helper.get()

    assert result == json.loads(RESPONSE)


def test_create(mock_requests_post):
    token = 'token'
    url = 'http://localhost:3000'
    http_helper = HttpHelper(token, url)

    result = http_helper.create({})

    assert result == json.loads(RESPONSE)


def test_update(mock_requests_patch):
    token = 'token'
    url = 'http://localhost:3000'
    http_helper = HttpHelper(token, url)

    result = http_helper.update(1, {})

    assert result == json.loads(RESPONSE)


def test_delete(mock_requests_delete):
    token = 'token'
    url = 'http://localhost:3000'
    http_helper = HttpHelper(token, url)

    result = http_helper.delete(1)

    assert result == json.loads(RESPONSE)
