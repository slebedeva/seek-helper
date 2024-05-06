import pytest
import json
from unittest import mock
from seek_helper.experiments.assay import Assay

GET_RESPONSE = '{"data":[{"id":"1","type":"assays","attributes":{"title":"Assay Example 1"},"links":{"self":"/assays/1"}},{"id":"2","type":"assays","attributes":{"title":"Assay Example 2"},"links":{"self":"/assays/2"}}],"jsonapi":{"version":"1.0"},"links":{"self":"/assays?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","first":"/assays?page%5Bnumber%5D=1&page%5Bsize%5D=1000000","prev":null,"next":null,"last":"/assays?page%5Bnumber%5D=1&page%5Bsize%5D=1000000"},"meta":{"base_url":"http://localhost:3000","api_version":"0.3"}}'
POST_RESPONSE = '{"data":{"id":"2","type":"assays","attributes":{"policy":{"access":"no_access","permissions":[]},"discussion_links":[],"snapshots":[],"title":"Assay Example","description":"This is an example of assay creation","other_creators":null,"position":null,"assay_class":{"title":"Experimental assay","key":"EXP","description":null},"assay_type":{"label":"Transcriptomics","uri":"http://jermontology.org/ontology/JERMOntology#Transcriptomics"},"technology_type":{"label":"TechnologyType","uri":"http://jermontology.org/ontology/JERMOntology#Technology_type"},"tags":[],"creators":[]},"relationships":{"creators":{"data":[]},"submitter":{"data":[{"id":"1","type":"people"}]},"organisms":{"data":[]},"human_diseases":{"data":[]},"people":{"data":[{"id":"1","type":"people"}]},"projects":{"data":[{"id":"1","type":"projects"}]},"investigation":{"data":{"id":"1","type":"investigations"}},"study":{"data":{"id":"1","type":"studies"}},"data_files":{"data":[]},"samples":{"data":[]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"placeholders":{"data":[]},"documents":{"data":[]}},"links":{"self":"/assays/2"},"meta":{"created":"2024-05-02T09:01:03.000Z","modified":"2024-05-02T09:01:03.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"6da75f60-ea90-013c-5750-00155d0fd7d9"}},"jsonapi":{"version":"1.0"}}'
PATCH_RESPONSE = '{"data":{"id":"2","type":"assays","attributes":{"policy":{"access":"no_access","permissions":[{"resource":{"id":"1","type":"projects"},"access":"download"}]},"discussion_links":[],"snapshots":[],"title":"Assay Example","description":"This is an example of assay update","other_creators":"","position":null,"assay_class":{"title":"Experimental assay","key":"EXP","description":null},"assay_type":{"label":"ExperimentalAssayType","uri":"http://jermontology.org/ontology/JERMOntology#Experimental_assay_type"},"technology_type":{"label":"TechnologyType","uri":"http://jermontology.org/ontology/JERMOntology#Technology_type"},"tags":[],"creators":[]},"relationships":{"creators":{"data":[{"id":"1","type":"people"}]},"submitter":{"data":[{"id":"1","type":"people"}]},"organisms":{"data":[]},"human_diseases":{"data":[]},"people":{"data":[{"id":"1","type":"people"}]},"projects":{"data":[{"id":"1","type":"projects"}]},"investigation":{"data":{"id":"1","type":"investigations"}},"study":{"data":{"id":"1","type":"studies"}},"data_files":{"data":[{"id":"1","type":"data_files"}]},"samples":{"data":[]},"models":{"data":[]},"sops":{"data":[]},"publications":{"data":[]},"placeholders":{"data":[]},"documents":{"data":[]}},"links":{"self":"/assays/2"},"meta":{"created":"2024-04-03T15:24:57.000Z","modified":"2024-05-02T09:09:44.000Z","api_version":"0.3","base_url":"http://localhost:3000","uuid":"40e58980-d3fc-013c-780a-00155ddef5bd"}},"jsonapi":{"version":"1.0"}}'
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
def assay():
    return Assay('token', 'http://localhost:3000')


class TestAssay:
    def test_get(self, assay):
        result = assay.get()

        assert result == json.loads(GET_RESPONSE)

    def test_create(self, assay):
        payload = {
            'data': {
                'type': 'assays',
                'attributes': {
                    'title': 'Assay Example',
                    'assay_class': {
                        'key': 'EXP',
                    },
                    'assay_type': {
                        'uri': 'http://jermontology.org/ontology/JERMOntology#Transcriptomics',
                    },
                    'description': 'This is an example of assay creation',
                },
                'relationships': {
                    'study': {
                        'data': {
                            'id': '1',
                            'type': 'studies',
                        }
                    },
                }
            }
        }

        result = assay.create(payload)

        assert result == json.loads(POST_RESPONSE)
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['title'] == payload['data']['attributes']['title']
        assert result['data']['attributes']['description'] == payload['data']['attributes']['description']
        assert result['data']['attributes']['assay_class']['key'] == payload['data']['attributes']['assay_class']['key']
        assert result['data']['attributes']['assay_type']['uri'] == payload['data']['attributes']['assay_type']['uri']
        assert result['data']['relationships']['study']['data']['id'] == payload['data']['relationships']['study']['data']['id']
        assert result['data']['relationships']['study']['data']['type'] == payload['data']['relationships']['study']['data']['type']

    def test_update(self, assay):
        payload = {
            'data': {
                'id': '2',
                'type': 'assays',
                'attributes': {
                    'description': 'This is an example of assay update',
                },
            }
        }

        result = assay.update(2, payload)

        assert result == json.loads(PATCH_RESPONSE)
        assert result['data']['id'] == payload['data']['id']
        assert result['data']['type'] == payload['data']['type']
        assert result['data']['attributes']['description'] == payload['data']['attributes']['description']

    def test_delete(self, assay):
        result = assay.delete(1)

        assert result == json.loads(DELETE_RESPONSE)
