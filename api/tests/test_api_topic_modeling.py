from rest_framework.test import APITestCase

from helpers.deep import get_processed_data
from helpers.create_classifier import create_classifier_model
from classifier.models import ClassifiedDocument


class TestTopicModelingAPI(APITestCase):
    """
    Tests for Topic Modeling API
    """
    def setUp(self):
        self.url = '/api/topic-modeling/'

    def test_no_params(self):
        params = {}
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "No params should be a bad request"
        data = response.json()
        assert 'documents' in data
        assert 'number_of_topics' in data
        assert 'keywords_per_topic' in data
        assert 'depth' in data

    def test_no_documents(self):
        params = {'number_of_topics': 2, 'keywords_per_topic': 2, 'depth': 1}
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "Should be a bad request"
        data = response.json()
        assert 'documents' in data
        assert 'number_of_topics' not in data
        assert 'keywords_per_topic' not in data
        assert 'depth' not in data

    def test_no_depth(self):
        params = {
            'documents': [
                'This is to be classified',
                'This is to be classified',
                'This is to be classified',
                ],
            # 'depth': 1,
            'number_of_topics': 3,
            'keywords_per_topic': 2
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "Should be a bad request"
        data = response.json()
        assert 'depth' in data
        assert 'documents' not in data
        assert 'keywords_per_topic' not in data
        assert 'number_of_topics' not in data

    def test_no_number_of_topics(self):
        params = {
            'documents': [
                'This is to be classified',
                'This is to be classified',
                'This is to be classified',
                ],
            'depth': 1,
            # 'number_of_topics': 3,
            'keywords_per_topic': 2
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "Should be a bad request"
        data = response.json()
        assert 'number_of_topics' in data
        assert 'documents' not in data
        assert 'keywords_per_topic' not in data
        assert 'depth' not in data

    def test_no_keywords_per_topic(self):
        params = {
            'documents': [
                'This is to be classified',
                'This is to be classified',
                'This is to be classified',
                ],
            'depth': 1,
            'number_of_topics': 3,
            # 'keywords_per_topic': 2
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "Should be a bad request"
        data = response.json()
        assert 'keywords_per_topic' in data
        assert 'documents' not in data
        assert 'number_of_topics' not in data
        assert 'depth' not in data

    def test_api_with_documents_depth1(self):
        params = {
            'documents': [
                'This is to be classified',
                'This is to be classified',
                'This is to be classified',
                ],
            'depth': 1,
            'number_of_topics': 3,
            'keywords_per_topic': 2
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 200
        data = response.json()
        # Check data structure for depth 1
        assert isinstance(data, dict)
        assert len(data.keys()) == params['number_of_topics']
        for name, topic in data.items():
            assert 'keywords' in topic
            assert isinstance(topic['keywords'], list)
            for kw in topic['keywords']:
                assert isinstance(kw, list)
                assert len(kw) == 2
                assert isinstance(kw[0], str)
                assert isinstance(kw[1], int) or isinstance(kw[1], float)
            assert 'subtopics' in topic
            assert not topic['subtopics'], "Subtopics should be empty"

    def test_api_with_documents_depth2(self):
        params = {
            'documents': [
                'This is to be classified',
                'This is to be classified',
                'This is to be classified',
                ],
            'depth': 2,
            'number_of_topics': 3,
            'keywords_per_topic': 2
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 200
        data = response.json()
        # Check data structure for depth 2
        depth2 = False  # topic with depth 2 found
        assert isinstance(data, dict)
        assert len(data.keys()) == params['number_of_topics']
        for name, topic in data.items():
            assert 'keywords' in topic
            assert isinstance(topic['keywords'], list)
            for kw in topic['keywords']:
                assert isinstance(kw, list)
                assert len(kw) == 2
                assert isinstance(kw[0], str)
                assert isinstance(kw[1], int) or isinstance(kw[1], float)
            assert 'subtopics' in topic
            sdata = topic['subtopics']
            assert isinstance(sdata, dict)
            if len(sdata.keys()) == params['number_of_topics']:
                depth2 = True
                for name, topic in sdata.items():
                    assert 'keywords' in topic
                    assert isinstance(topic['keywords'], list)
                    for kw in topic['keywords']:
                        assert isinstance(kw, list)
                        assert len(kw) == 2
                        assert isinstance(kw[0], str)
                        assert isinstance(kw[1], int) or\
                            isinstance(kw[1], float)
                    assert 'subtopics' in topic
        assert depth2, "At least one topic should have depth 2"
