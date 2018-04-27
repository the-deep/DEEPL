from rest_framework.test import APITestCase
from django.conf import settings

from clustering.tasks import create_new_clusters

import os


class TestClusteringAPI(APITestCase):
    """
    Tests for clustering API
    """
    fixtures = [
        'fixtures/classifier.json',
        'fixtures/test_classified_docs.json',
        'fixtures/test_base_models.json',
    ]

    def setUp(self):
        # first create clusters
        self.cluster_data_path = 'test_clusters/'
        # create path if not exist
        os.system('mkdir -p {}'.format(self.cluster_data_path))
        os.environ[settings.ENVIRON_CLUSTERING_DATA_LOCATION] = \
            self.cluster_data_path
        # set values
        self.group_id = '1'
        self.num_clusters = 2
        self.api_url = '/api/clustering/'
        self.valid_params = {
            'group_id': self.group_id,
            'num_clusters': self.num_clusters
        }

    def test_no_group_id(self):
        params = {}
        response = self.client.post(self.api_url, params)
        assert response.status_code == 400, "No group_id is a bad request."
        data = response.json()
        assert 'group_id' in data

    def test_invalid_num_clusters(self):
        params = {'group_id': '1'}
        invalids = [None, 'abc', '  ', 'bibek', 1.1, -3, '1.10']
        for invalid in invalids:
            if invalids is not None:
                params['num_clusters'] = invalid
            response = self.client.post(self.api_url, params)
            assert response.status_code == 400,\
                "No num_clusters is a bad request."
            data = response.json()
            assert 'num_clusters' in data

    def test_create_cluster_first_request_api(self):
        """Test when cluster_create request is sent"""
        params = self.valid_params
        response = self.client.post(self.api_url, params)
        data = response.json()
        print(data)
        assert response.status_code == 202, "No data returned but accepted"
        data = response.json()
        assert 'message' in data

    def test_clustered_prepared_resposne(self):
        # create a clustered model
        cluster_model = create_new_clusters(
            "test_cluster", self.group_id, 2
        )
        params = self.valid_params
        response = self.client.post(self.api_url, params)
        assert response.status_code == 201
        data = response.json()
        data = response.json()
        assert 'cluster_id' in data
        assert isinstance(data['cluster_id'], int)
        assert data['cluster_id'] == cluster_model.id

    def test_get_cluster_invalid_model_id(self):
        params = {}
        invalids = [None, "abcd", "1.1", "-1"]
        for invalid in invalids:
            if invalid is not None:
                params['model_id'] = invalid
            response = self.client.get(self.api_url, params)
            assert response.status_code == 400, "no model_id should be 400"
            data = response.json()
            assert 'model_id' in data

    def test_get_cluster_non_existent_model_id(self):
        params = {'model_id': 9876543}
        response = self.client.get(self.api_url, params)
        print(response.json())
        assert response.status_code == 404, "non existent model_id is 404"
        data = response.json()
        assert 'message' in data

    def test_get_cluster(self):
        cluster_model = create_new_clusters(
            "test_cluster", self.group_id, 2
        )
        params = {'model_id': cluster_model.id}
        response = self.client.get(self.api_url, params)
        assert response.status_code == 200
        data = response.json()
        assert 'score' in data
        assert data['score'] >= -1 and data['score'] <= 1
        assert 'doc_ids' in data
        assert isinstance(data['doc_ids'], list)
        for did in data['doc_ids']:
            isinstance(did, int)
        assert 'relevant_terms' in data
        for term in data['relevant_terms']:
            assert isinstance(term, str)
        assert 'group_id' in data
        assert isinstance(data['group_id'], str)

    def tearDown(self):
        # remove test cluster folder
        os.system('rm -r {}'.format(self.cluster_data_path))
