from rest_framework.test import APITestCase


class TestFuzzyCountrySearchAPI(APITestCase):
    """
    Tests for Fuzzy API
    """
    def setUp(self):
        self.fuzzy_url = '/api/fuzzy-search/{}/'
        self.api_url = self.fuzzy_url.format('country')

    def test_search_invalid_type(self):
        invalid_types = ['nothing', 'anything', 'human']
        for type in invalid_types:
            url = self.fuzzy_url.format(type)
            response = self.client.get(url, {})
            assert response.status_code == 404
            data = response.json()
            assert 'message' in data

    def test_no_query(self):
        params = {}
        response = self.client.get(self.api_url, params)
        assert response.status_code == 400, 'query should be present'
        data = response.json()
        assert 'query' in data

    def test_invalid_query(self):
        invalid_queries = [  # queries should have min length 3
            '', 'a', '1', '       ', '\n\n\n', '\r\r\r\n', '\r\n'
        ]
        params = {}
        for invalid in invalid_queries:
            params['query'] = invalid
            response = self.client.get(self.api_url, params)
            assert response.status_code == 400, 'Query length should be 3 or more'  # noqa
            data = response.json()
            assert 'query' in data

    def test_valid_query(self):
        params = {'query': 'india'}
        response = self.client.get(self.api_url, params)
        assert response.status_code == 200, 'There should be a result'
        data = response.json()
        assert isinstance(data, dict)
        assert 'matches' in data
        for match in data['matches']:
            assert isinstance(match, dict)
            assert 'label' in match
            assert 'similarity' in match
            sim = match['similarity']
            assert isinstance(sim, int) or isinstance(sim, float)
            assert 'extra' in match
            assert isinstance(match['extra'], dict)
            assert 'iso2' in match['extra']
            assert 'iso3' in match['extra']
