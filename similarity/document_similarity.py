import math
import numpy as np

from helpers.common import preprocess
from similarity.helpers import (
    get_indexed_terms,
    get_term_frequencies,
    get_inverse_frequencies,
    get_number_of_documents
)
from classifier.models import ClassifiedDocument


class DocumentSimilarityModel:
    """
    Class for calculating similarities between two documents
    """
    def __init__(self):
        # get all the indices
        self.terms_indices = get_indexed_terms()
        self.term_freqs = get_term_frequencies()
        self.inverse_freqs = get_inverse_frequencies()
        self.terms_len = len(self.terms_indices.keys())
        self.total_docs = get_number_of_documents()

    def get_text_vector(self, text):
        processed = preprocess(text, ignore_numbers=True)
        text_terms = {}
        # fill in text_terms first
        for x in processed.split():
            text_terms[x] = text_terms.get(x, 0.0) + 1
        vector = [0.0] * self.terms_len
        for k, v in text_terms.items():
            termid = self.terms_indices.get(k)
            # only if the term is already in our index
            if termid:
                inv_freq = self.inverse_freqs.get(termid, 0)
                idf = 0 if not inv_freq else\
                    math.log(self.total_docs/float(inv_freq))
                vector[self.terms_indices[k]] = v * idf
        return vector

    @staticmethod
    def cosine_smilarity(vec1, vec2):
        """
        Return the cosine of the two vectors
        """
        # first convert them to numpy array
        if not isinstance(vec1, np.ndarray):
            vec1 = np.array(vec1)
        if not isinstance(vec2, np.ndarray):
            vec2 = np.array(vec2)
        n1 = vec1 / np.linalg.norm(vec1)
        n2 = vec2 / np.linalg.norm(vec2)
        dot = np.dot(n1, n2)
        if np.isnan(dot):
            return 0.0
        return dot

    def documents_similarity(self, doc1, doc2):
        v1 = self.get_text_vector(doc1)
        v2 = self.get_text_vector(doc2)
        return self.cosine_smilarity(v1, v2)

    def get_document_vector(self, docid):
        """Get vector for the document with given docid.
        Will get ClassifiedDocument object.
        """
        try:
            doc = ClassifiedDocument.objects.get(id=docid)
        except ClassifiedDocument.DoesNotExist:
            return None
        else:
            return self.get_text_vector(doc.text)
