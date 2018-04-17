import matplotlib
matplotlib.use('Agg')
import json
import os
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from django.conf import settings

from clustering.models import ClusteringModel
from clustering.kmeans_doc2vec import KMeansDoc2Vec
from helpers.utils import Resource, uncompress_compressed_vector


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.
    '''
    return plt.cm.get_cmap(name, n)


def visualize_clusters(model, plottype):
    print("Getting features and labels...")
    nfeatures = 3 if plottype == '3d' else 2
    reduced_features, labels, n_clusters = get_docs_features_labels(
        model, nfeatures
    )
    print("Plotting clusters...")
    # Plot
    fig = plot(reduced_features, labels, n_clusters, plottype)
    # get location of clusters data
    resource = Resource(
        settings.ENVIRON_CLUSTERING_DATA_LOCATION,
        Resource.FILE_AND_ENVIRONMENT
    )
    path = os.path.join(
        resource.get_resource_location(),
        'cluster_model_{}'.format(model.id)
    )
    filepath = os.path.join(path, 'clusterplot.png')
    print("Saving plot to {}".format(filepath))
    fig.savefig(filepath)


def get_docs_features_labels(model, nfeatures):
    modelid = model.id
    # get location of clusters data
    resource = Resource(
        settings.ENVIRON_CLUSTERING_DATA_LOCATION,
        Resource.FILE_AND_ENVIRONMENT
    )
    path = os.path.join(
        resource.get_resource_location(),
        'cluster_model_{}'.format(modelid)
    )
    labels_path = os.path.join(path, settings.CLUSTERED_DOCS_LABELS_FILENAME)
    labels_resource = Resource(labels_path, Resource.FILE)
    labels_data = json.loads(labels_resource.get_data())
    zipped = [(docid, data) for docid, data in labels_data.items()]

    n_clusters = model.n_clusters
    # Now get documents dimensions
    docs_features, docs_labels = [], []
    if isinstance(model.model, KMeansDoc2Vec):
        def identity(x): return x
        features_uncompress_function = identity
    else:
        features_uncompress_function = uncompress_compressed_vector
    for did, data in zipped:
        # first uncompress and then store
        docs_features.append(features_uncompress_function(data['features']))
        docs_labels.append(data['label'])
    reduced_features = reduce_dimensions(docs_features, nfeatures)
    print(reduced_features)
    return reduced_features, docs_labels, n_clusters


def plot(features, labels, num_clusters, plottype):
    # plot docs_features and docs_labels
    colormap = get_cmap(num_clusters)
    fig = plt.figure(figsize=(15, 8))
    plotter = plt
    if plottype == '3d':
        plotter = Axes3D(fig)
    for i, f in enumerate(features):
        colind = labels[i]
        plotter.scatter(*f, c=colormap(colind))
    return fig


def reduce_dimensions(data, dimension=3):
    clf = TruncatedSVD(dimension)
    transformed = clf.fit_transform(data)
    print(transformed.shape)
    return transformed


def main(*args, **kwargs):
    modelversion = kwargs.get('model_version')
    plottype = kwargs.get('plot_type')
    if plottype != '3d':
        plottype = '2d'
    if not modelversion:
        print("Error: model_version not provided. Usage: --model_version=<version>")
        return
    try:
        model = ClusteringModel.objects.get(version=modelversion)
    except ClusteringModel.DoesNotExist:
        print("No model with version {} found.".format(modelversion))
    visualize_clusters(model, plottype)
