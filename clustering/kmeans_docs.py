"""
=======================================
Clustering text documents using k-means
=======================================

This is an example showing how the scikit-learn can be used to cluster
documents by topics using a bag-of-words approach. This example uses
a scipy.sparse matrix to store the features instead of standard numpy arrays.

Two feature extraction methods can be used in this example:

  - TfidfVectorizer uses a in-memory vocabulary (a python dict) to map the most
    frequent words to features indices and hence compute a word occurrence
    frequency (sparse) matrix. The word frequencies are then reweighted using
    the Inverse Document Frequency (IDF) vector collected feature-wise over
    the corpus.

  - HashingVectorizer hashes word occurrences to a fixed dimensional space,
    possibly with collisions. The word count vectors are then normalized to
    each have l2-norm equal to one (projected to the euclidean unit-ball) which
    seems to be important for k-means to work in high dimensional space.

    HashingVectorizer does not provide IDF weighting as this is a stateless
    model (the fit method does nothing). When IDF weighting is needed it can
    be added by pipelining its output to a TfidfTransformer instance.

Two algorithms are demoed: ordinary k-means and its more scalable cousin
minibatch k-means.

Additionally, latent semantic analysis can also be used to reduce dimensionality
and discover latent patterns in the data.

It can be noted that k-means (and minibatch k-means) are very sensitive to
feature scaling and that in this case the IDF weighting helps improve the
quality of the clustering by quite a lot as measured against the "ground truth"
provided by the class label assignments of the 20 newsgroups dataset.

This improvement is not visible in the Silhouette Coefficient which is small
for both as this measure seem to suffer from the phenomenon called
"Concentration of Measure" or "Curse of Dimensionality" for high dimensional
datasets such as text data. Other measures such as V-measure and Adjusted Rand
Index are information theoretic based evaluation scores: as they are only based
on cluster assignments rather than distances, hence not affected by the curse
of dimensionality.

Note: as k-means is optimizing a non-convex objective function, it will likely
end up in a local optimum. Several runs with independent random init might be
necessary to get a good convergence.

"""

# Author: Peter Prettenhofer <peter.prettenhofer@gmail.com>
#         Lars Buitinck
# License: BSD 3 clause

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
                    max_df=0.5,
                    # max_features=self.options.n_features,
                    min_df=2, stop_words='english',
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
        print("Clustering done...\nreturning model")
        return self

    def get_silhouette_score(self):
        if self.silhouette_score is None:
            self.silhouette_score = silhouette_score(
                self.X, self.model.labels_, metric='euclidean'
            )
        return self.silhouette_score


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
