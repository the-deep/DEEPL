import json
import os
from sklearn.decomposition import PCA

from django.conf import settings

from clustering.models import ClusteringModel
from helpers.utils import Resource


def visualize_clusters(model):
    id = model.id
    # get location of clusters data
    resource = Resource(
        settings.ENVIRON_CLUSTERING_DATA_LOCATION,
        Resource.FILE_AND_ENVIRONMENT
    )
    path = os.path.join(
        resource.get_resource_location(),
        'cluster_model_{}'.format(id)
    )
    labels_path = os.path.join(path, settings.CLUSTERED_DOCS_LABELS_FILENAME)
    labels_resource = Resource(labels_path, Resource.FILE)
    labels_data = json.loads(labels_resource.get_data())
    print(model.model._check_fit_data())
    print(labels_data)


def main(*args, **kwargs):
    modelversion = kwargs.get('model_version')
    if not modelversion:
        print("Error: model_version not provided. Usage: --model_version=<version>")
        return
    try:
        model = ClusteringModel.objects.get(version=modelversion)
    except ClusteringModel.DoesNotExist:
        print("No model with version {} found.".format(modelversion))
    visualize_clusters(model)
