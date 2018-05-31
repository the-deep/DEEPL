from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans, MiniBatchKMeans

from clustering.base import ClusteringOptions, GenericClustering


class KMeansDocs(GenericClustering):
    """
    The class which clusters the documents
    """
    def __init__(self, options=ClusteringOptions()):
        self.options = options
        self.explained_variance = None
        self.cluster_centers = None
        self.model = None
        self.silhouette_score = None
        self.X = None

    def perform_cluster(self, documents):
        # documents should be cleaned docs
        if self.options.use_hashing:
            if self.options.use_idf:
                # Perform an IDF normalization on output of HashingVectorizer
                hasher = HashingVectorizer(
                        n_features=self.options.n_features,
                        stop_words='english', alternate_sign=False,
                        norm=None, binary=False)
                vectorizer = make_pipeline(hasher, TfidfTransformer())
            else:
                vectorizer = HashingVectorizer(
                        n_features=self.options.n_features,
                        stop_words='english',
                        alternate_sign=False, norm='l2',
                        binary=False)
        else:
            vectorizer = TfidfVectorizer(
                    max_df=100,
                    # max_features=self.options.n_features,
                    min_df=1, stop_words='english',
                    use_idf=self.options.use_idf)
        self.vectorizer = vectorizer
        X = vectorizer.fit_transform(documents)

        self.lsa_transformer = None
        if self.options.n_components:
            svd = TruncatedSVD(self.options.n_components)
            normalizer = Normalizer(copy=False)
            lsa = make_pipeline(svd, normalizer)
            self.lsa_transformer = lsa
            X = lsa.fit_transform(X)
            self.explained_variance = svd.explained_variance_ratio_.sum()

        if self.options.minibatch:
            km = MiniBatchKMeans(
                    n_clusters=self.options.n_clusters, init='k-means++',
                    n_init=1, init_size=1000, batch_size=1000)
        else:
            km = KMeans(
                n_clusters=self.options.n_clusters,
                init='k-means++', max_iter=100, n_init=1
            )
        self.model = km
        km.fit(X)
        self.X = X
        self.cluster_centers = km.cluster_centers_
        return self

    def update_cluster(self, documents):
        # documents should be cleaned docs
        X = self.vectorizer.fit_transform(documents)
        self.model.partial_fit(X)
        self.X = X
        # NOTE: self.model.labels_ will be updated to have only latest labels

    def get_silhouette_score(self):
        if self.silhouette_score is None:
            self.silhouette_score = silhouette_score(
                self.X, self.model.labels_, metric='euclidean'
            )
        return self.silhouette_score

    def get_doc_features(self, document):
        if self.vectorizer is None:
            raise Exception("Clustering has not been done. Run perform_cluster() first.")
        return self.vectorizer.fit_transform([document])[0]


def _processed_docs():
    import csv
    docs = []
    with open('/home/bibek/projects/DEEPL/fixtures/processed_data_for_testing.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            docs.append(row['excerpt'])
    return docs


if __name__ == '__main__':
    options = ClusteringOptions(n_clusters=3)
    kmeans = KMeansDocs(options)
    # get docs
    docs = _processed_docs()
    kmeans.perform_cluster(docs)
    print(kmeans.model.cluster_centers_)
    print(kmeans.model.labels_)
    print(set(kmeans.model.labels_))
