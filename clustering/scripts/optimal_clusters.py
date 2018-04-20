from sklearn.metrics import silhouette_score

from clustering.base import ClusteringOptions
from clustering.kmeans_docs import KMeansDocs
from clustering.kmeans_doc2vec import KMeansDoc2Vec
from clustering.models import Doc2VecModel
from classifier.models import ClassifiedDocument
from helpers.utils import timeit


@timeit
def find_optimal_clusters(
        min_clusters=2,
        max_clusters=20,
        CLUSTER_CLASS=KMeansDocs,
        doc2vec_group_id=None):
    max_silhouette = -1.0  # to compare with
    clusters = 1
    if CLUSTER_CLASS == KMeansDocs:
        docs = ClassifiedDocument.objects.all().values('id', 'text')
        texts = list(map(lambda x: x['text'], docs))
        cluster_params = texts
    elif CLUSTER_CLASS == KMeansDoc2Vec:
        # get Doc2VecModel
        doc2vecmodel = Doc2VecModel.objects.get(group_id=doc2vec_group_id)
        cluster_params = [x for x in doc2vecmodel.model.docvecs]
    else:
        raise Exception("Invalid class")
    for n in range(min_clusters, max_clusters + 1):
        if n > len(cluster_params) - 1:
            break
        options = ClusteringOptions(n_clusters=n, store_X=True)
        k_means = CLUSTER_CLASS(options)
        kmeans_model = k_means.perform_cluster(cluster_params)
        labels = kmeans_model.model.labels_
        silhouette = silhouette_score(k_means.X, labels, metric='euclidean')
        print("n_clusters {}, silhouette_score {}".format(n, silhouette))
        if silhouette >= max_silhouette:
            max_silhouette = silhouette
            clusters = n
    return clusters, max_silhouette


def main(*args, **kwargs):
    cluster_method = kwargs.get('cluster_method')
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
    # clustering method
    if not cluster_method or cluster_method == 'bow':
        kargs['CLUSTER_CLASS'] = KMeansDocs
    elif cluster_method == 'doc2vec':
        kargs['CLUSTER_CLASS'] = KMeansDoc2Vec
        doc2vec_group_id = kwargs.get('doc2vec_group_id')
        if not doc2vec_group_id:
            print('Provide --doc2vec_group_id for clustring with doc2vec')
            return
        kargs['doc2vec_group_id'] = doc2vec_group_id
    else:
        print("Invalid cluster method. Valid methods: --cluster_method=[doc2vec|bow]")
        return

    optimal, score = find_optimal_clusters(**kargs)
    print("The optimal number of clusters for dataset is {} with silhouette score of {}".format(optimal, score))
