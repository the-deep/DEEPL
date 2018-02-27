from rest_framework.test import APITestCase

from helpers.deep import get_processed_data
from helpers.create_classifier import create_classifier_model


class TestClassificationAPI(APITestCase):
    """
    Tests for text classification API
    """
    def setUp(self):
        self.classifier_model = self._get_model()
        self.classifier_model.save()
        # TODO: And create some classified docs as well
        self.url = '/api/v1/classify/'

    def itest_no_text_and_deeper_param(self):
        params = {}
        resposne = self.post()

    def test_api_with_text(self):
        params = {'text': 'This is to be classified'}
        response = self.client.post(self.url, params)
        assert response.status_code == 200
        data = response.json()
        assert "classification" in data
        assert "classification_confidence" in data
        assert type(data['classification']) == list
        # Just to check if list contains tuples, if not exception raised
        for label, prob in data['classification']:
            pass

    def test_api_with_text_deeper(self):
        params = {'text': 'This is to be classified', 'deeper': '1'}
        response = self.client.post(self.url, params)
        assert response.status_code == 200
        data = response.json()
        assert "group_id" in data
        assert "id" in data
        assert "classification" in data
        assert "classification_confidence" in data
        assert type(data['classification']) == list
        # Just to check if list contains tuples, if not exception raised
        for label, prob in data['classification']:
            pass
        assert 'excerpts_classification' in data
        for x in data['excerpts_classification']:
            assert 'start_pos' in x, "Start pos not in excerpt"
            assert 'end_pos' in x, "End pos not in excerpt"
            assert 'classification' in x, "classification not in excerpt"
            assert 'classification_confidence' in x, \
                "classification_confidence not in excerpt"

    def _get_model(self):
        # first create classifier
        csv_path = 'fixtures/processed_data_for_testing.csv'
        data = get_processed_data(csv_path)
        return create_classifier_model(1, data)

    def _create_classified_docs(self, classifier_model):
        classifier = classifier_model.classifier
        texts = []


def assertion_structure_data(structure, data):
    # TODO: complete this
    data = {
        'classification': [(str, str)],
        'classification_confidence': float,
        'id': int,
        'excerpts_classification': [{
            'classification': [(str, str)],
            'classification_confidence': float,
            'start_pos': int,
            'end_pos': int,
        }]
    }
    assert type(structure) == type(data)
    if type(structure) == list:
        pass
