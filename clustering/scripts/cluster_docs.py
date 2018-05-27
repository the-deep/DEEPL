
from django.db import transaction

from classifier.models import ClassifiedDocument
from clustering.models import ClusteringModel
from clustering.kmeans_docs import KMeansDocs
from clustering.kmeans_doc2vec import KMeansDoc2Vec
from clustering.tasks import create_new_clusters
from helpers.utils import timeit


@timeit
def create_document_clusters(
        name, group_id, n_clusters,
        CLUSTER_CLASS=KMeansDocs, doc2vec_group_id=None, recreate=True
        ):
    """
    Create document clusters(ClusteringModel object) based on input params
    @name: name of the model
    @group_id: group_id of the model
    @CLUSTER_CLASS: class on which the clustring(KMeans) is based
    @doc2vec_group_id: relevant if clusterclass is KMeansDoc2Vec, get doc2vec
        model and load vectors from it
    """
    # first check if group_id already exists or not
    try:
        ClusteringModel.objects.get(group_id=group_id)
        if not recreate:
            raise Exception(
                "Cluster model with group_id {} already exists".format(
                    group_id)
            )
    except ClusteringModel.DoesNotExist:
        pass
        # create new clustering model
    create_new_clusters(
        name, group_id, n_clusters, CLUSTER_CLASS, doc2vec_group_id
    )


@timeit
def create_clusters(num_clusters):
    groups = ClassifiedDocument.objects.all().values('group_id').\
            distinct()
    for g in groups:
        gid = g['group_id']
        create_document_clusters(
            'Cluster for {}'.format(gid), gid, num_clusters
        )


def main(*args, **kwargs):
    # TODO: get num_clusters from args
    modelname = kwargs.get('model_name')
    modelgroup_id = kwargs.get('group_id')
    cluster_method = kwargs.get('cluster_method')
    try:
        num_clusters = int(kwargs.get('num_clusters'))
    except (ValueError, TypeError):
        print("Empty/invalid number of clusters. Usage: --num_clusters <int>")
        return

    if not modelname and not modelgroup_id:  # means create all clusters
        # prompt user for confirmation as this will override all clusters
        yn = input('Are you sure you want to re/create all clusters? Doing this will override existing clusters.(y/n)')  # noqa
        if yn.lower() == 'y':
            create_clusters(num_clusters)
        else:
            print('Operation cancelled. Provide other options to cluster specific clusters')  # noqa
        return
    if not modelname:
        print("Model name not provided. Provide it with: --model_name <name>")
        return
    if not modelgroup_id:
        print("Model group_id not provided. Provide it with: --group_id\
<group_id>")
        return

    doc2vec_group_id = None  # only relevant if cluster_method is doc2vec
    # clustering method
    if not cluster_method or cluster_method == 'bow':
        cluster_class = KMeansDocs
    elif cluster_method == 'doc2vec':
        cluster_class = KMeansDoc2Vec
        doc2vec_group_id = kwargs.get('doc2vec_group_id')
        if not doc2vec_group_id:
            print('Provide --doc2vec_group_id for clustring with doc2vec')
            return
    else:
        print("Invalid cluster method. Valid methods: --cluster_method=[doc2vec|bow]")  # noqa
        return

    try:
        with transaction.atomic():
            create_document_clusters(
                modelname, modelgroup_id, num_clusters,
                cluster_class, doc2vec_group_id
            )
    except Exception as e:
        raise e
