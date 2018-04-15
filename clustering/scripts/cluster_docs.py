import json
import os
import subprocess

from django.conf import settings
from django.db import transaction

from classifier.models import ClassifiedDocument
from clustering.kmeans_docs import KMeansDocs, ClusteringOptions
from clustering.models import ClusteringModel
from helpers.utils import timeit, Resource, compress_sparse_vector


@timeit
def create_document_clusters(name, version, n_clusters):
    # first check if version already exists or not
    try:
        ClusteringModel.objects.get(version=version)
        raise Exception("Cluster model with version {} already exists".format(
            version))
    except ClusteringModel.DoesNotExist:
        pass
    print("Getting documents")
    docs = ClassifiedDocument.objects.all().values('id', 'text')
    texts = list(map(lambda x: x['text'], docs))
    docids = list(map(lambda x: x['id'], docs))
    options = ClusteringOptions(n_clusters=n_clusters)

    k_means = KMeansDocs(options)
    print("Creating clustering model")
    kmeans_model = k_means.perform_cluster(texts)
    docs_labels = zip(docids,  # convert from np.int64 to int
                      list(map(lambda x: int(x), kmeans_model.model.labels_)))

    # Save to database
    cluster_model = ClusteringModel()
    cluster_model.model = kmeans_model
    cluster_model.name = name
    cluster_model.version = version
    cluster_model.n_clusters = n_clusters
    print("Saving model to database")
    cluster_model.silhouette_score = kmeans_model.get_silhouette_score()
    cluster_model.save()
    # Now write to files
    print("Writing results to files")
    write_clustured_data_to_files(
        cluster_model,
        docs_labels,
        kmeans_model.model.cluster_centers_,
        docs
    )


def write_clustured_data_to_files(
        model, docs_labels, cluster_centers, docs
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
    vectorizer = model.model.vectorizer
    for doc in docs:
        arr = vectorizer.fit_transform([doc['text']]).toarray()[0]
        compressed = compress_sparse_vector(arr)
        dict_data[doc['id']]['features'] = compressed
    # Write docs_clusterlabels
    labels_resource.write_data(json.dumps(dict_data))
    print("Done writing data")


def main(*args, **kwargs):
    # TODO: get num_clusters from args
    modelname = kwargs.get('model_name')
    modelversion = kwargs.get('model_version')
    if not modelname:
        print("Model name not provided. Provide it with: --model_name <name>")
        return
    if not modelversion:
        print("Model version not provided. Provide it with: --model_version\
<version>")
        return
    try:
        num_clusters = int(kwargs.get('num_clusters'))
    except (ValueError, TypeError):
        print("Empty/invalid number of clusters. Usage: --num_clusters <int>")
        return
    try:
        with transaction.atomic():
            create_document_clusters(modelname, modelversion, num_clusters)
    except Exception as e:
        raise e
