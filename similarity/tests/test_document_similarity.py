import unittest
import os
from django.conf import settings

from similarity.document_similarity import DocumentSimilarityModel
from similarity.helpers import (
    get_indexed_terms,
    get_term_frequencies_data,
    get_inverse_frequencies,
    get_number_of_documents
)
from helpers.common import preprocess


class TestDocumentSimilarityModel(unittest.TestCase):
    """
    Testing of various similarity usecases
    """
    def setUp(self):
        # change os.environ variable, because loading real indices takes time
        test_indices_path = os.path.join(
            os.path.dirname(settings.BASE_DIR), 'nlp_data/test_indices'
        )
        os.environ[settings.INDICES_PATH_ENV_VAR] = test_indices_path
        self.similarity_model = DocumentSimilarityModel()

    def test_similarity_two_texts(self):
        # First preprocess  documents
        doc1 = "This is test. Aeroplane flight"
        doc2 = "This is test"
        doc1 = preprocess(doc1)
        doc2 = preprocess(doc2)
        similarity = self.similarity_model.documents_similarity(doc1, doc2)
        assert isinstance(similarity, float)

    def test_get_text_vector(self):
        text = "exact record runway crash"
        vec = self.similarity_model.get_text_vector(text)
        assert isinstance(vec, list)
        print(self.similarity_model.terms_len)
        assert len(vec) == self.similarity_model.terms_len
        for x in vec:
            assert isinstance(x, float)
        print(vec)
        assert any(vec), "Not all dimensions can be zero"

    def test_cosine_similarity(self):
        vec1, vec2 = [6, 7], [3, 5]
        similarity = self.similarity_model.cosine_smilarity(vec1, vec2)
        assert round(similarity, 5) == 0.98589
        similarity = self.similarity_model.cosine_smilarity(vec2, vec1)
        assert round(similarity, 5) == 0.98589
        vec1, vec2 = [1, 3, 5], [0.4, 0.7, 0.8]
        similarity = self.similarity_model.cosine_smilarity(vec2, vec1)
        assert round(similarity, 5) == 0.96735

    def test_document_similarity(self):
        # NOTE: the texts should contain words in our test indices
        # otherwise the similarity will be nan
        doc1 = "Prime minister from China has leadership"
        doc2 = "This is just a dummy text. Pilot flies aeroplane"
        similarity = self.similarity_model.documents_similarity(doc1, doc2)
        assert isinstance(similarity, float)
        assert similarity >= 0.0, "Similarity should always be >= 0"


class TestSimilarityHelpers(unittest.TestCase):
    """
    Testing of various helpers functions for similarity
    """
    def setUp(self):
        pass

    def test_get_indexed_terms(self):
        terms = get_indexed_terms()
        for t, i in terms.items():
            assert isinstance(t, str)
            assert isinstance(i, int)

    def test_get_term_frequencies_data(self):
        data = get_term_frequencies_data()
        assert isinstance(data, dict)
        assert 'num_docs' in data
        assert 'docs_tf' in data
        assert isinstance(data['num_docs'], int)
        for t, f in data['docs_tf'].items():
            assert isinstance(f, dict)
            for k, v in f.items():
                assert isinstance(k, int)
                assert isinstance(v, int)

    def test_get_inverse_frequencies(self):
        invfreqs = get_inverse_frequencies()
        for t, f in invfreqs.items():
            assert isinstance(t, int)
            assert isinstance(f, int)

    # NO need to test this now, get_term_frequencies_data gives it
    def itest_get_number_of_documents(self):
        num = get_number_of_documents()
        assert isinstance(num, int)
