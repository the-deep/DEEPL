from rest_framework.test import APITestCase

from classifier.models import ClassifiedDocument


class TestSummarization(APITestCase):
    """
    Test cases for summarization API
    """
    fixtures = [
        'fixtures/test_base_models.json',
        'fixtures/classifier.json',
        'fixtures/test_classified_docs.json',
    ]

    def setUp(self):
        self.url = '/api/summarization/'
        self.doc = ClassifiedDocument.objects.last()

    def test_no_params(self):
        resp = self.client.get(self.url, {})
        assert resp.status_code == 400
        data = resp.json()
        # either of the following should be present
        assert 'doc_id' in data
        assert 'text' in data

    def test_non_existent_doc_id(self):
        params = {'doc_id': 99999}
        resp = self.client.get(self.url, params)
        assert resp.status_code == 404
        data = resp.json()
        assert 'message' in data

    def test_invalid_doc(self):
        invalids = [
            '', '  \r\n', '\r', '\n',
            'This is very short. Should fail very badly. Else algorithm bug']
        for invalid in invalids:
            params = {'text': invalid}
            resp = self.client.get(self.url, params)
            assert resp.status_code == 400
            data = resp.json()
            assert 'text' in data

    def test_valid_doc_id(self):
        params = {'doc_id': self.doc.id}
        resp = self.client.get(self.url, params)
        assert resp.status_code == 200
        data = resp.json()
        assert 'summary' in data
        assert isinstance(data['summary'], str)

    def test_valid_text(self):
        params = {
            'text': '''After having some sleepless nights(I am insomniac sometimes) and re-preparations after the first exam, on the day of second exam, I collected my admit card, pen, pencil, calculator and went to the examination centre in Dhapakhel.
A bit nervous, a bit excited and a bit happy(because I would be free from preparations that day), I reached the exam centre which was Kantipur Engineering College, a beautiful place. I met my friends, excited and happy. We had some talks about how we were quite nervous and excited and how we had prepared for that exam.
            '''
        }
        resp = self.client.get(self.url, params)
        assert resp.status_code == 200
        data = resp.json()
        assert 'summary' in data
        assert isinstance(data['summary'], str)
