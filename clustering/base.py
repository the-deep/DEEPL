class NotImplementedError(Exception):
    pass


class ClusteringOptions:
    """
    Object that stores info about how the model is created
    """
    def __init__(
            self, n_clusters=8, use_hashing=True, use_idf=False,
            n_components=None, minibatch=False, n_features=1000,
            store_X=False
            ):
        self.n_clusters = n_clusters
        self.n_features = n_features
        self.use_hashing = use_hashing
        self.use_idf = use_idf
        self.n_components = n_components  # for dimensionality reduction
        self.minibatch = minibatch
        self.store_X = store_X


class GenericClustering:

    def perform_cluster(self, documents):
        raise NotImplementedError

    def get_silhouette_score(self):
        raise NotImplementedError
