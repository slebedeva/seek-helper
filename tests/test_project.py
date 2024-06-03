import pytest
import json
from unittest import mock
from seek_helper.yellow_pages.project import Project

GET_RESPONSE = '{"data":{"id":"1","type":"projects","attributes":{"discussion_links":[],"avatar":null,"title":"Default Project","description":null,"web_page":null,"wiki_page":null,"default_license":"CC-BY-4.0","start_date":null,"end_date":null,"members":[{"person_id":"1","institution_id":"1"}],"topic_annotations":[]},"relationships":{"project_administrators":{"data":[]},"pals":{"data":[]},"asset_housekeepers":{"data":[]},"asset_gatekeepers":{"data":[]},"organisms":{"data":[]},"human_diseases":{"data":[]},"people":{"data":[{"id":"1","type":"people"}]},"institutions":{"data":[{"id":"1","type":"institutions"}]},"programmes":{"data":[]},"investigations":{"data":[{"id":"1","type":"investigations"}]},"studies":{"data":[{"id":"1","type":"studies"}]},"assays":{"data":[{"id":"1","type":"assays"}]},"data_files":{"data":[{"id":"1","type":"data_files"}]},"file_templates":{"data":[]},"placeholders":{"data":[]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"presentations":{"data":[]},"events":{"data":[]},"documents":{"data":[]},"workflows":{"data":[]},"collections":{"data":[]}},"links":{"self":"/projects/1"},"meta":{"created":"2024-03-26T14:24:04.000Z","modified":"2024-03-26T14:25:14.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"6c0b1c00-cdaa-013c-c442-00155dee8a98"}},"jsonapi":{"version":"1.0"}}'
POST_RESPONSE = '{"data":{"id":"2","type":"projects","attributes":{"discussion_links":[],"avatar":null,"title":"Project Example","description":"This is an example of project creation","web_page":null,"wiki_page":null,"default_license":"CC-BY-4.0","start_date":null,"end_date":null,"members":[],"topic_annotations":[]},"relationships":{"project_administrators":{"data":[]},"pals":{"data":[]},"asset_housekeepers":{"data":[]},"asset_gatekeepers":{"data":[]},"organisms":{"data":[]},"human_diseases":{"data":[]},"people":{"data":[]},"institutions":{"data":[]},"programmes":{"data":[]},"investigations":{"data":[]},"studies":{"data":[]},"assays":{"data":[]},"data_files":{"data":[]},"file_templates":{"data":[]},"placeholders":{"data":[]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"presentations":{"data":[]},"events":{"data":[]},"documents":{"data":[]},"workflows":{"data":[]},"collections":{"data":[]}},"links":{"self":"/projects/2"},"meta":{"created":"2024-05-01T16:00:21.000Z","modified":"2024-05-01T16:00:21.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"d67e1e90-ea01-013c-f529-00155d343140"}},"jsonapi":{"version":"1.0"}}'
PATCH_RESPONSE = '{"data":{"id":"2","type":"projects","attributes":{"discussion_links":[],"avatar":null,"title":"Project Example","description":"This is an example of project update","web_page":null,"wiki_page":null,"default_license":"CC-BY-4.0","start_date":null,"end_date":null,"members":[{"person_id":"1","institution_id":"1"}],"topic_annotations":[]},"relationships":{"project_administrators":{"data":[]},"pals":{"data":[]},"asset_housekeepers":{"data":[]},"asset_gatekeepers":{"data":[]},"organisms":{"data":[]},"human_diseases":{"data":[]},"people":{"data":[{"id":"1","type":"people"}]},"institutions":{"data":[{"id":"1","type":"institutions"}]},"programmes":{"data":[]},"investigations":{"data":[{"id":"1","type":"investigations"},{"id":"2","type":"investigations"}]},"studies":{"data":[{"id":"1","type":"studies"}]},"assays":{"data":[{"id":"1","type":"assays"},{"id":"2","type":"assays"}]},"data_files":{"data":[{"id":"1","type":"data_files"}]},"file_templates":{"data":[]},"placeholders":{"data":[]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"presentations":{"data":[]},"events":{"data":[]},"documents":{"data":[]},"workflows":{"data":[]},"collections":{"data":[]}},"links":{"self":"/projects/2"},"meta":{"created":"2024-03-26T14:24:04.000Z","modified":"2024-05-02T08:27:53.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"6c0b1c00-cdaa-013c-c442-00155dee8a98"}},"jsonapi":{"version":"1.0"}}'
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
def project():
    return Project('token', 'http://localhost:3000', 'input/path', mock.Mock())


class TestProject:
    def test_get(self, project):
        result = project.get()

        assert result == json.loads(GET_RESPONSE)

    def test_create(self, project):
        payload = {
            'data': {
                'type': 'projects',
                'attributes': {
                    'title': 'Project Example',
                    'description': 'This is an example of project creation',
                },
            }
        }

        result = project.create(payload)

        assert result == json.loads(POST_RESPONSE)
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['title'] == payload['data']['attributes']['title']
        assert result['data']['attributes']['description'] == payload['data']['attributes']['description']

    def test_update(self, project):
        payload = {
            'data': {
                'id': '2',
                'type': 'projects',
                'attributes': {
                    'description': 'This is an example of project update',
                },
            }
        }

        result = project.update(2, payload)

        assert result == json.loads(PATCH_RESPONSE)
        assert result['data']['id'] == payload['data']['id']
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['description'] == payload['data']['attributes']['description']

    def test_delete(self, project):
        result = project.delete(1)

        assert result == json.loads(DELETE_RESPONSE)

    # TODO: test_download_data_files

    # TODO: test_upload_data_files
