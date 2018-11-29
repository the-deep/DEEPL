from rest_framework.test import APITestCase

from classifier.models import ClassifiedDocument
from helpers.deep import get_processed_data
from helpers.create_classifier import create_classifier_model

from api.tests.utils import with_token_auth_tests
from NER.models import NERCache
from NER.ner import get_ner_tagging_doc


@with_token_auth_tests
class TestNERAPI(APITestCase):
    """
    Tests for Keywords Named Entity Recognition API
    """
    def setUp(self):
        self.url = '/api/ner/'

    def test_ner_no_params(self):
        params = {}
        response = self.client.post(self.url, params)
        assert response.status_code == 400
        data = response.json()
        assert 'text' in data

    def test_ner(self):
        params = {
            'text': '''Mount Everest lies in Nepal. Edmund Hillary conquered it
            first with Tenzing Norgey Sherpa.'''
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 200
        data = response.data
        assert isinstance(data, list)
        for x in data:
            assert 'entity' in x
            assert 'length' in x
            assert 'start' in x


@with_token_auth_tests
class TestNERwithDocsAPI(APITestCase):
    """
    Tests for Keywords Named Entity Recognition API
    """
    fixtures = [
        'fixtures/classifier.json',
        'fixtures/test_classified_docs.json',
        'fixtures/test_base_models.json',
    ]

    def setUp(self):
        self.url = '/api/ner-docs/'
        self.classified_doc = ClassifiedDocument.objects.last()
        NERCache.objects.all().delete()

    def test_ner_docs_no_params(self):
        params = {}
        response = self.client.post(self.url, params)
        assert response.status_code == 400
        data = response.json()
        assert 'doc_ids' in data

    def test_ner_docs_404(self):
        """
        Send 404 if none of the document_ids match
        """
        params = {'doc_ids': [999, 1111, 300]}
        response = self.client.post(self.url, params)
        print(response.json())
        assert response.status_code == 404, \
            "No documents matched should give 404"

    def itest_ner_doc_ids(self):
        # NOTE: this is ignored as it non-deterministically passes and fails
        params = {
            'doc_ids': [self.classified_doc.id]
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 200
        data = response.data
        assert isinstance(data, dict)
        assert 'locations' in data
        locations = data['locations']
        assert isinstance(locations, list)
        for location in locations:
            assert 'name' in location
            assert 'info' in location
            info = location['info']
            assert 'types' in info
            assert isinstance(info['types'], list)
            assert 'address_components' in info
            assert isinstance(info['address_components'], list)
            for comp in info['address_components']:
                assert 'types' in comp
                assert isinstance(comp['types'], list)
                assert 'short_name' in comp
                assert 'long_name' in comp
            assert 'geometry' in info
            assert 'place_id' in info
            assert 'formatted_address' in info
            geometry = info['geometry']
            assert 'location_type' in geometry
            assert 'bounds' in geometry
            assert 'northeast' in geometry['bounds']
            assert 'lat' in geometry['bounds']['northeast']
            assert 'lng' in geometry['bounds']['northeast']
            assert 'southwest' in geometry['bounds']
            assert 'lat' in geometry['bounds']['southwest']
            assert 'lng' in geometry['bounds']['southwest']
            assert 'location' in geometry
            assert 'lat' in geometry['location']
            assert 'lng' in geometry['location']
            assert 'viewport' in geometry

    def itest_location_cached(self):
        params = {
            'doc_ids': [self.classified_doc.id]
        }
        # first post and then again post to check cached key
        response = self.client.post(self.url, params)
        # now again post to check for cached key in info
        response = self.client.post(self.url, params)
        data = response.json()
        assert isinstance(data, dict)
        assert 'locations' in data
        locations = data['locations']
        assert isinstance(locations, list)
        for location in locations:
            assert 'name' in location
            assert 'info' in location
            assert 'cached' in location['info']
            assert location['info']['cached'] is True

    def test_ner_not_cached(self):
        # first remove cache
        NERCache.objects.all().delete()
        params = {
            'doc_ids': [self.classified_doc.id]
        }
        response = self.client.post(self.url, params)
        data = response.json()
        assert isinstance(data, dict)
        assert 'locations' in data
        # assert 'cached' in data
        # assert data['cached'] is False
        locations = data['locations']
        assert isinstance(locations, list)
        for location in locations:
            assert 'name' in location
            assert 'info' in location
            assert 'cached' in location['info']

    def test_ner_cached(self):
        # first remove cache
        NERCache.objects.all().delete()
        # create cache
        get_ner_tagging_doc(self.classified_doc.id)
        params = {
            'doc_ids': [self.classified_doc.id]
        }
        response = self.client.post(self.url, params)
        data = response.json()
        assert isinstance(data, dict)
        assert 'locations' in data
        # assert 'cached' in data
        # assert data['cached'] is False
        locations = data['locations']
        assert isinstance(locations, list)
        for location in locations:
            assert 'name' in location
            assert 'info' in location
            assert 'cached' in location['info']

    def _get_model(self, version):
        # first create classifier
        csv_path = 'fixtures/processed_data_for_testing.csv'
        data = get_processed_data(csv_path)
        return create_classifier_model(version, data)
