from rest_framework.test import APITestCase


class TestKeywordsExtractionAPI(APITestCase):
    """
    Tests for Keywords Extraction api
    """
    def setUp(self):
        self.url = '/api/keywords-extraction/'

    def test_extraction_no_params(self):
        params = {}
        response = self.client.post(self.url, params)
        assert response.status_code == 400
        data = response.json()
        assert 'document' in data

    def test_invalid_max_grams(self):
        params = {
            'document': 'This is a test document',
        }
        invalid_max_grams = ['abc', '-1', '1.3']
        for max_grams in invalid_max_grams:
            params['max_grams'] = max_grams
            response = self.client.post(self.url, params)
            assert response.status_code == 400
            data = response.json()
            assert 'document' not in data
            assert 'max_grams' in data

    def test_extraction_api(self):
        params = {
            'document': 'This is a document whose keywords are for extraction',
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 200
        data = response.json()
        # check ngrams upto 3, if no numbers specified, defaults to 3
        for x in range(3):
            key = '{}grams'.format(x+1)
            assert key in data
            for x in data[key]:
                assert type(x) == list
                assert len(x) == 2

    def test_extraction_api_max_grams(self):
        params = {
            'document': 'This is a document whose keywords are for extraction',
            'max_grams': 4
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 200
        data = response.json()
        # check ngrams upto params['max_grams']
        for x in range(params['max_grams']):
            key = '{}grams'.format(x+1)
            assert key in data
            for x in data[key]:
                assert type(x) == list
                assert len(x) == 2

    def test_extraction_include_numbers(self):
        params = {
            'document': '''This is 2018 a document whose keywords are for
            keywords extraction.
            ''',
            'include_numbers': 'true'
        }
        response = self.client.post(self.url, params)
        assert response.status_code == 200
        data = response.json()
        assert '1grams' in data
        kws = list(map(lambda x: x[0], data['1grams']))
        assert '2018' in kws, "Numbers should be present"

    def test_extraction_no_include_numbers(self):
        params = {
            'document': '''This is 2018 a document whose keywords are for
            keywords extraction.
            ''',
        }
        # list of values that mean don't include numbers
        no_include_vals = ['false', '0', 0, 'abc']
        for val in no_include_vals:
            params['include_numbers'] = val
            response = self.client.post(self.url, params)
            assert response.status_code == 200
            data = response.json()
            assert '1grams' in data
            kws = list(map(lambda x: x[0], data['1grams']))
            assert '2018' not in kws, "Numbers should not be present"
