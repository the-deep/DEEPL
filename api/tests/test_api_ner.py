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
        assert 'entities' in data


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
        assert response.status_code == 404, "No documents matched should give 404"

    def test_ner_doc_ids(self):
        params = {
            'doc_ids': [self.classified_doc.id]
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 200
        data = response.data
        assert 'entities' in data

    def _get_model(self, version):
        # first create classifier
        csv_path = 'fixtures/processed_data_for_testing.csv'
        data = get_processed_data(csv_path)
        return create_classifier_model(version, data)
