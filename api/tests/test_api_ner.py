from rest_framework.test import APITestCase

from classifier.models import ClassifiedDocument
from helpers.deep import get_processed_data
from helpers.create_classifier import create_classifier_model


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


class TestNERwithDocsAPI(APITestCase):
    """
    Tests for Keywords Named Entity Recognition API
    """
    def setUp(self):
        self.url = '/api/ner-docs/'
        self.classifier_model = self._get_model(1)
        self.classifier_model.save()
        txt = "Kathmandu is the capital of Nepal; Mohummad Ali was a boxer"
        self.classified_doc = ClassifiedDocument.objects.create(
            text="Kathmandu is the capital of Nepal; Mohummad Ali was a boxer",
            classifier=self.classifier_model,
            confidence=0.2,
            classification_label="ABC",
            classification_probabilities=self.classifier_model.classifier.
                classify_as_label_probs(txt)
        )

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

    def test_cached(self):
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

    def _get_model(self, version):
        # first create classifier
        csv_path = 'fixtures/processed_data_for_testing.csv'
        data = get_processed_data(csv_path)
        return create_classifier_model(version, data)
