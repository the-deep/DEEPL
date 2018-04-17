from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from clustering.base import GenericClustering, ClusteringOptions


class KMeansDoc2Vec(GenericClustering):
    """
    Perform kmeans clustering with word2vec
    """
    def __init__(self, options=ClusteringOptions()):
        self.options = options
        self.explained_variance = None
        self.cluster_centers = None
        self.model = None
        self.silhouette_score = None

    def perform_cluster(self, docVectors):
        """
        Input parameter is document vectors
        """
        km = KMeans(
            n_clusters=self.options.n_clusters, init='k-means++',
            max_iter=100, n_init=1
        )
        km.fit(docVectors)
        self.model = km
        self.X = docVectors
        self.cluster_centers = km.cluster_centers_
        print("Clustering done...\nreturning model")
        return self

    def get_silhouette_score(self):
        if self.silhouette_score is None:
            self.silhouette_score = silhouette_score(
                self.X, self.model.labels_, metric='euclidean'
            )
        return self.silhouette_score


if __name__ == '__main__':
    sentences = [
        ['this', 'is', 'the', 'good', 'machine', 'learning', 'book'],
        ['this', 'is',  'another', 'book'],
        ['one', 'more', 'book'],
        ['this', 'is', 'the', 'new', 'post'],
        ['this', 'is', 'about', 'machine', 'learning', 'post'],
        ['and', 'this', 'is', 'the', 'last', 'post']
    ]
