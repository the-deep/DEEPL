from rest_framework.test import APITestCase

from classifier.models import ClassifiedDocument
from topic_modeling.models import TopicModelingModel
from topic_modeling.tasks import get_topics_and_subtopics_task

from api.tests.utils import with_token_auth_tests


@with_token_auth_tests
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


@with_token_auth_tests
class TestTopicModelingAPIV2(APITestCase):
    """Test cases for v2 topic modeling api"""
    fixtures = [
        'fixtures/test_base_models.json',
        'fixtures/classifier.json',
        'fixtures/test_classified_docs.json',
    ]

    def setUp(self):
        self.url = '/api/v2/topic-modeling/'
        self.group_id = ClassifiedDocument.objects.last().group_id

    def test_invalid_version(self):
        url = self.url.replace('2', '3')
        params = {}  # does not matter as params validation does not take place
        response = self.client.post(url, params)
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
        assert 'version' in data['error']
        # Now test for GET
        response = self.client.get(url, params)
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
        assert 'version' in data['error']

    def test_no_group_id(self):
        params = {
            'depth': 1,
            'number_of_topics': 3,
            'keywords_per_topic': 2
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 400
        data = response.json()
        assert 'group_id' in data
        # test get
        response = self.client.get(self.url, params)
        assert response.status_code == 400
        data = response.json()
        assert 'group_id' in data

    def test_non_existent_group_id(self):
        params = {
            'group_id': 'This does not exist',
            'depth': 1,
            'number_of_topics': 3,
            'keywords_per_topic': 2
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 404
        data = response.json()
        assert 'message' in data

    def test_no_depth(self):
        params = {
            'group_id': self.group_id,
            'number_of_topics': 3,
            'keywords_per_topic': 2
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "Should be a bad request"
        data = response.json()
        assert 'depth' in data
        assert 'keywords_per_topic' not in data
        assert 'number_of_topics' not in data
        # Test for GET
        response = self.client.get(self.url, params)
        assert response.status_code == 400, "Should be a bad request"
        data = response.json()
        assert 'depth' in data
        assert 'keywords_per_topic' not in data
        assert 'number_of_topics' not in data

    def test_no_number_of_topics(self):
        params = {
            'depth': 1,
            'group_id': self.group_id,
            'keywords_per_topic': 2
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "Should be a bad request"
        data = response.json()
        assert 'number_of_topics' in data
        assert 'keywords_per_topic' not in data
        assert 'depth' not in data
        # test for GET
        response = self.client.get(self.url, params)
        assert response.status_code == 400, "Should be a bad request"
        data = response.json()
        assert 'number_of_topics' in data
        assert 'keywords_per_topic' not in data
        assert 'depth' not in data

    def test_no_keywords_per_topic(self):
        params = {
            'depth': 1,
            'number_of_topics': 3,
            'group_id': self.group_id
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "Should be a bad request"
        data = response.json()
        assert 'keywords_per_topic' in data
        assert 'number_of_topics' not in data
        assert 'depth' not in data
        # test for GET
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "Should be a bad request"
        data = response.json()
        assert 'keywords_per_topic' in data
        assert 'number_of_topics' not in data
        assert 'depth' not in data

    def test_topic_modeling_post_new(self):
        params = {
            'group_id': self.group_id,
            'depth': 1,
            'number_of_topics': 3,
            'keywords_per_topic': 2
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 202, "Model will be created in bg"
        # get topic model and check status is not ready
        model = TopicModelingModel.objects.get(group_id=self.group_id)
        assert not model.ready

    def test_topic_modeling_get_no_model_exists(self):
        params = {
            'group_id': self.group_id,
            'depth': 1,
            'number_of_topics': 3,
            'keywords_per_topic': 2
        }
        response = self.client.get(self.url, params)
        assert response.status_code == 404, "Model is not yet created"
        data = response.json()
        assert 'message' in data  # Message is about initiating model creation

    def test_topic_modeling_get_not_ready(self):
        params = {
            'group_id': self.group_id,
            'depth': 1,
            'number_of_topics': 3,
            'keywords_per_topic': 2
        }
        # first post
        self.client.post(self.url, params)
        response = self.client.get(self.url, params)
        assert response.status_code == 202, "Model is still not ready"

    def test_topic_modeling_get_ready(self):
        params = {
            'group_id': self.group_id,
            'depth': 1,
            'number_of_topics': 3,
            'keywords_per_topic': 2
        }
        # call post first
        self.client.post(self.url, params)
        # create the model, this is the background task done by celery
        get_topics_and_subtopics_task(
            params['group_id'],
            params['number_of_topics'],
            params['keywords_per_topic'],
            params['depth']
        )
        response = self.client.get(self.url, params)
        assert response.status_code == 200
        data = response.json()
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
            assert not topic['subtopics']  # only one depth


class TestTopicsCorrelation(APITestCase):
    """Test cases for topic correlation"""
    fixtures = [
        'fixtures/test_base_models.json',
        'fixtures/classifier.json',
        'fixtures/test_classified_docs.json',
    ]

    def setUp(self):
        self.url = '/api/topics/correlation/'
        self.group_id = ClassifiedDocument.objects.last().group_id

    def test_no_group_id(self):
        params = {}
        resp = self.client.post(self.url, params)
        assert resp.status_code == 400
        data = resp.json()
        assert 'group_id' in data

    def test_topic_correlation_not_ready(self):
        params = {'group_id': self.group_id}
        resp = self.client.post(self.url, params)
        assert resp.status_code == 202
        data = resp.json()
        assert 'message' in data

    def test_topic_correlation_ready(self):
        params = {'group_id': self.group_id}
        # create a model, whose content will be returned by the api
        get_topics_and_subtopics_task(self.group_id)
        resp = self.client.post(self.url, params)
        assert resp.status_code == 200
        data = resp.json()
        assert 'topics_correlation' in data
        correlation = data['topics_correlation']
        assert isinstance(correlation, dict)
        for k, v in correlation.items():
            assert isinstance(v, dict)
            for kk, vv in v.items():
                assert isinstance(vv, float)
