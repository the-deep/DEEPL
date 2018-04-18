import json
import os
import subprocess

from django.conf import settings
from django.db import transaction

from classifier.models import ClassifiedDocument
from clustering.base import ClusteringOptions
from clustering.kmeans_docs import KMeansDocs
from clustering.kmeans_doc2vec import KMeansDoc2Vec
from clustering.models import ClusteringModel, Doc2VecModel
from helpers.utils import timeit, Resource, compress_sparse_vector


@timeit
def create_document_clusters(
        name, group_id, n_clusters,
        CLUSTER_CLASS=KMeansDocs, doc2vec_group_id=None
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
        raise Exception("Cluster model with group_id {} already exists".format(
            group_id))
    except ClusteringModel.DoesNotExist:
        pass
    print("Getting documents")

    options = ClusteringOptions(n_clusters=n_clusters)

    if CLUSTER_CLASS == KMeansDocs:
        docs = ClassifiedDocument.objects.all().values('id', 'text')
        texts = list(map(lambda x: x['text'], docs))
        docids = list(map(lambda x: x['id'], docs))
        cluster_params = texts
    elif CLUSTER_CLASS == KMeansDoc2Vec:
        # get Doc2VecModel
        doc2vecmodel = Doc2VecModel.objects.get(group_id=doc2vec_group_id)
        cluster_params = [x for x in doc2vecmodel.model.docvecs]
        docids = doc2vecmodel.model.docvecs.doctags.keys()
        features = cluster_params
    else:
        raise Exception("Invalid class")

    k_means = CLUSTER_CLASS(options)
    print("Creating clustering model")
    kmeans_model = k_means.perform_cluster(cluster_params)
    docs_labels = zip(docids,  # convert from np.int64 to int
                      list(map(lambda x: int(x), kmeans_model.model.labels_)))

    # Save to database
    cluster_model = ClusteringModel()
    cluster_model.model = kmeans_model
    cluster_model.name = name
    cluster_model.group_id = group_id
    cluster_model.n_clusters = n_clusters
    print("Saving model to database")
    cluster_model.silhouette_score = kmeans_model.get_silhouette_score()
    cluster_model.save()

    # create features for KMeansDocs
    if CLUSTER_CLASS == KMeansDocs:
        features = []
        vectorizer = kmeans_model.vectorizer
        for txt in texts:
            arr = vectorizer.fit_transform([txt]).toarray()[0]
            compressed = compress_sparse_vector(arr)
            features.append(compressed)

    docids_features = dict(zip(docids, features))
    # Now write to files
    print("Writing results to files")
    write_clustured_data_to_files(
        cluster_model,
        docs_labels,
        kmeans_model.model.cluster_centers_,
        docids_features
    )


def write_clustured_data_to_files(
        model, docs_labels, cluster_centers, docids_features
        ):
    """Write the doc_clusterlabels and cluster_centers to files"""
    cluster_data_location = settings.ENVIRON_CLUSTERING_DATA_LOCATION
    resource = Resource(
        cluster_data_location,
        Resource.FILE_AND_ENVIRONMENT
    )
    # create another resource(folder to keep files)
    path = os.path.join(
        resource.get_resource_location(),
        'cluster_model_{}'.format(model.id)
    )
    # create the directory
    p = subprocess.Popen(['mkdir', '-p', path], stdout=subprocess.PIPE)
    _, err = p.communicate()
    if err:
        print("Couldn't create cluster data files. {}".format(err))
        return
    # now create centers file
    center_path = os.path.join(path, settings.CLUSTERS_CENTERS_FILENAME)
    center_resource = Resource(center_path, Resource.FILE)
    # convert to python float first or it won't be json serializable
    centers_data = {
        i: compress_sparse_vector([float(y) for y in x])
        for i, x in enumerate(cluster_centers)
    }
    center_resource.write_data(json.dumps(centers_data))
    # now create labels file
    labels_path = os.path.join(path, settings.CLUSTERED_DOCS_LABELS_FILENAME)
    labels_resource = Resource(labels_path, Resource.FILE)
    # create dict
    dict_data = {x: {'label': y} for x, y in docs_labels}
    for doc_id, features in docids_features.items():
        # first make json serializable
        dict_data[doc_id]['features'] = [
            float(x) if isinstance(model.model, KMeansDoc2Vec) else x
            for x in features
        ]
        print(dict_data)
    # Write docs_clusterlabels
    labels_resource.write_data(json.dumps(dict_data))
    print("Done writing data")


def main(*args, **kwargs):
    # TODO: get num_clusters from args
    modelname = kwargs.get('model_name')
    modelgroup_id = kwargs.get('group_id')
    cluster_method = kwargs.get('cluster_method')
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
        print("Invalid cluster method. Valid methods: --cluster_method=[doc2vec|bow]")
        return

    try:
        num_clusters = int(kwargs.get('num_clusters'))
    except (ValueError, TypeError):
        print("Empty/invalid number of clusters. Usage: --num_clusters <int>")
        return
    try:
        with transaction.atomic():
            create_document_clusters(
                modelname, modelgroup_id, num_clusters,
                cluster_class, doc2vec_group_id
            )
    except Exception as e:
        raise e
