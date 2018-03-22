import unittest
import os
from django.conf import settings

from similarity.document_similarity import DocumentSimilarityModel
from similarity.helpers import (
    get_indexed_terms,
    get_term_frequencies,
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
            os.path.dirname(settings.BASE_DIR), 'test_indices'
        )
        os.environ[settings.INDICES_PATH_ENV_VAR] = test_indices_path
        self.similarity_model = DocumentSimilarityModel()

    def test_similarity_two_texts(self, doc1, doc2):
        # First preprocess  documents
        doc1 = preprocess(doc1)
        doc2 = preprocess(doc2)
        similarity = self.similarity_model.get_similarity(doc1, doc2)
        assert isinstance(similarity, float)

    def test_get_text_vector(self):
        text = "this is some random text. this is runway"
        vec = self.similarity_model.get_text_vector(text)
        assert isinstance(vec, list)
        for x in vec:
            assert isinstance(x, float)
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

    def test_get_germ_frequencies(self):
        freqs = get_term_frequencies()
        # data should be {termid: {docid: freq}, ... }
        for t, f in freqs.items():
            assert isinstance(f, dict)
            for k, v in f.items():
                assert isinstance(k, int)
                assert isinstance(v, int)

    def test_get_inverse_frequencies(self):
        invfreqs = get_inverse_frequencies()
        for t, f in invfreqs.items():
            assert isinstance(t, int)
            assert isinstance(f, int)

    def test_get_number_of_documents(self):
        num = get_number_of_documents()
        assert isinstance(num, int)
