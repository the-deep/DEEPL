from sklearn.metrics import silhouette_score

from clustering.kmeans_docs import KMeansDocs, ClusteringOptions
from classifier.models import ClassifiedDocument
from helpers.utils import timeit


@timeit
def find_optimal_clusters(min_clusters=2, max_clusters=20):
    # fetch texts first
    docs = ClassifiedDocument.objects.all().values('id', 'text')
    texts = list(map(lambda x: x['text'], docs))
    last_silhouette = -1.0  # to compare with
    for n in range(min_clusters, max_clusters + 1):
        options = ClusteringOptions(n_clusters=n, store_X=True)
        k_means = KMeansDocs(options)
        kmeans_model = k_means.perform_cluster(texts)
        labels = kmeans_model.model.labels_
        silhouette = silhouette_score(k_means.X, labels, metric='euclidean')
        if silhouette < last_silhouette:
            return n - 1, last_silhouette
        last_silhouette = silhouette
    return max_clusters, last_silhouette


def main(*args, **kwargs):
    try:
        min_clusters = int(kwargs['min_clusters'])
        if min_clusters < 0:
            raise ValueError
    except (ValueError, KeyError) as e:
        print('WARNING: non integral value for min_clusters, using default')
        min_clusters = None
    try:
        max_clusters = int(kwargs['max_clusters'])
        if max_clusters < 0:
            raise ValueError
    except (ValueError, KeyError) as e:
        print('WARNING: non integral value for max_clusters, using default')
        max_clusters = None
    kargs = {}
    if min_clusters:
        kargs['min_clusters'] = min_clusters
    if max_clusters:
        kargs['max_clusters'] = max_clusters

    optimal, score = find_optimal_clusters(**kargs)
    print("The optimal number of clusters for dataset is {} with silhouette score of {}".format(optimal, score))
