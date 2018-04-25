import unittest

from clustering.base import ClusteringOptions
from clustering.kmeans_docs import KMeansDocs


class TestKMeansDocs(unittest.TestCase):
    def setUp(self):
        self.documents = [
            "this is a test document that is to be tested for various NLP algorithms.",
            "document classification and clustering is a very important task in NLP",
            "Computers are these days almost as important as electricity",
            "Not only computers are important, they are part of life as well"
        ]
        self.clustering_options = ClusteringOptions(n_clusters=2)

    def test_creation_kmeans_docs(self):
        kmeansdocs = KMeansDocs(self.clustering_options)
        km = kmeansdocs.perform_cluster(self.documents)
        assert km == kmeansdocs
        assert km.X is not None
        sc = km.get_silhouette_score()
        assert sc >= -1 and sc <= 1
