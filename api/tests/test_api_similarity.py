from rest_framework.test import APITestCase

from similarity.globals import set_similarity_model
from classifier.models import ClassifiedDocument, ClassifierModel


class iTestDocsSimilarityAPI(APITestCase):
    """
    API tests for documents similarity
    """
    def setUp(self):
        set_similarity_model()  # this will initialize global similarity_model
        self.valid_params = {
            'doc1': 'This is a valid doc that uses words from text indices like\
 pilot, leadership, country, etc',
            'doc2': 'This is another valid doc. and prime minister from china \
has leadership'
        }
        self.url = '/api/similarity/'

    def test_no_params(self):
        params = dict(self.valid_params)
        del params['doc1']
        del params['doc2']
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "No params should be a bad request"
        data = response.json()
        assert 'doc1' in data
        assert 'doc2' in data

    def test_empty_doc1(self):
        params = dict(self.valid_params)
        params['doc1'] = '  '
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "Empty doc should be a bad request"
        data = response.json()
        assert 'doc1' in data

    def test_empty_doc2(self):
        params = dict(self.valid_params)
        params['doc2'] = '  '
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "Empty doc should be a bad request"
        data = response.json()
        assert 'doc2' in data

    def test_valid_docs(self):
        response = self.client.post(self.url, self.valid_params)
        assert response.status_code == 200, "Should be a valid request"
        data = response.json()
        assert 'similarity' in data
        assert isinstance(data['similarity'], float)
        # NOTE: in fact the value below should be greater than 0, depends on
        #  dataset
        assert data['similarity'] >= 0.0, "Some words overlap so similarity sho\
uld be greater than/equal to 0"


class TestSimilarDocsAPI(APITestCase):
    """
    API tests for similar docs
    """
    fixtures = [
        'fixtures/test_base_models.json',
        'fixtures/classifier.json'
    ]

    def setUp(self):
        self.classifier_model = ClassifierModel.objects.get(version=1)
        texts = [
            "Foreign prime minister flies aeroplane with a pilot",
            "There is no pilot in the flight"
        ]
        # create classified docs
        self.doc_id = None
        for t in texts:
            obj = ClassifiedDocument.objects.create(
                text=t,
                classifier=self.classifier_model,
                confidence=0.2,  # this is just a value, not relevant here
                classification_label="ABC",
                classification_probabilities=self.classifier_model.classifier.
                    classify_as_label_probs(t)
            )
            self.doc_id = obj.id
        self.url = '/api/similardocs/'

    def test_no_params(self):
        params = {}
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "No params should be a bad request"
        data = response.json()
        assert 'doc_id' in data
        assert 'doc' in data

    def test_invalid_docid(self):
        invalids = ['1.2', 'abc', '-12', '', '   ']
        params = {}
        for invalid in invalids:
            params['doc_id'] = invalid
            response = self.client.post(self.url, params)
            assert response.status_code == 400, "Invalid doc_id should be 400"
            data = response.json()
            assert 'doc_id' in data

    def test_non_existing_docid(self):
        params = {'doc_id': 99999}  # 99999 doesn't exist, we have only 2 in db
        response = self.client.post(self.url, params)
        assert response.status_code == 404, "Should be 404"
        data = response.json()
        assert 'error' in data

    def test_empty_doc(self):
        params = {'doc': ' '}
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "Empty doc should be a bad request"
        data = response.json()
        assert 'doc' in data

    def test_doc_and_no_group_id(self):
        params = {'doc': 'This is a test doc.'}
        response = self.client.post(self.url, params)
        assert response.status_code == 400, "No group_id should be 400 error"
        data = response.json()
        assert 'group_id' in data

    def test_with_valid_doc(self):
        params = {'doc': 'aeroplane, pilot  prime minister'}
        response = self.client.post(self.url, params)
        assert response.status_code == 200
        data = response.json()
        assert 'similar_docs' in data
        for x in data['similar_docs']:
            assert isinstance(x, list) or isinstance(x, tuple)
            assert len(x) == 2
            assert x[1] <= 1.0 and x[1] >= 0.0

    def test_with_valid_doc_id(self):
        params = {'doc_id': self.doc_id}  # we created two docs
        response = self.client.post(self.url, params)
        assert response.status_code == 200
        data = response.json()
        assert 'similar_docs' in data
        for x in data['similar_docs']:
            assert isinstance(x, list) or isinstance(x, tuple)
            assert len(x) == 2
            assert x[1] <= 1.0 and x[1] >= 0.0
