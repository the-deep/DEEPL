import json
import os
import subprocess

from django.conf import settings
from django.db import transaction

from classifier.models import ClassifiedDocument
from clustering.kmeans_docs import KMeansDocs, ClusteringOptions
from clustering.models import ClusteringModel
from helpers.utils import timeit, Resource


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
                      list(map(lambda x: int(x), kmeans_model.labels_)))
    # Save to database
    cluster_model = ClusteringModel()
    cluster_model.model = kmeans_model
    cluster_model.name = name
    cluster_model.version = version
    cluster_model.n_clusters = n_clusters
    print("Saving model to database")
    cluster_model_id = cluster_model.save()
    # Now write to files
    print("Writing results to files")
    write_clustured_data_to_files(
        cluster_model_id,
        docs_labels,
        kmeans_model.cluster_centers_
    )


def write_clustured_data_to_files(model_id, docs_labels, cluster_centers):
    """Write the doc_clusterlabels and cluster_centers to files"""
    cluster_data_location = settings.ENVIRON_CLUSTERING_DATA_LOCATION
    resource = Resource(
        cluster_data_location,
        Resource.FILE_AND_ENVIRONMENT
    )
    # create another resource(folder to keep files)
    path = os.path.join(
        resource.get_resource_location(),
        'cluster_model_{}'.format(model_id)
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
        i: [float(y) for y in x]
        for i, x in enumerate(cluster_centers)
    }
    center_resource.write_data(json.dumps(centers_data))
    # now create labels file
    labels_path = os.path.join(path, settings.CLUSTERED_DOCS_LABELS_FILENAME)
    labels_resource = Resource(labels_path, Resource.FILE)
    # Write docs_clusterlabels
    dict_data = dict(docs_labels)
    labels_resource.write_data(json.dumps(dict_data))
    print("Done writing data")


def main(*args, **kwargs):
    # TODO: get num_clusters from args
    modelname = kwargs.get('modelname')
    modelversion = kwargs.get('modelversion')
    if not modelname:
        print("Model name not provided. Provide it with: --modelname <name>")
        return
    if not modelversion:
        print("Model version not provided. Provide it with: --modelversion\
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
