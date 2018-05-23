import os
import json
import subprocess

from django.conf import settings

from helpers.utils import compress_sparse_vector, Resource
from clustering.kmeans_doc2vec import KMeansDoc2Vec


def write_or_update_centers_data(model, cluster_centers):
    """
    @model: ClusteringModel instance
    @cluster_centers: [<uncompressed_center_data>, ...]
    """
    path = model.get_cluster_data_path()
    center_path = os.path.join(path, settings.CLUSTERS_CENTERS_FILENAME)
    center_resource = Resource(center_path, Resource.FILE)
    # convert to python float first or it won't be json serializable
    centers_data = {
        i: compress_sparse_vector([float(y) for y in x])
        for i, x in enumerate(cluster_centers)
    }
    # Center data can be directly written whether update is true or false as
    # centers gets updated
    center_resource.write_data(json.dumps(centers_data))


def write_cluster_labels_data(
        model, docs_labels, docids_features, update=False
        ):
    """
    @model: ClusteringModel instance
    @docs_labels:[(<doc_id>, <label_id>), ...]
    @docids_features: { <doc_id>: <features>, ... }
    @update: False means replace the file contents, else just update
    """
    path = model.get_cluster_data_path()
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
    # Write docs_clusterlabels
    if update:
        data = json.loads(labels_resource.get_data())
        data.update(dict_data)
        labels_resource.write_data(json.dumps(data))
    else:
        labels_resource.write_data(json.dumps(dict_data))


def write_relevent_terms_data(model, relevant_terms, update=False):
    """
    @model: ClusteringModel instance
    @relevant_terms: { <cluster_label>: [<relevant_term>, ...], ...}
    @update: False means replace content in file
    """
    path = model.get_cluster_data_path()
    relevant_path = os.path.join(path, settings.RELEVANT_TERMS_FILENAME)
    relevant_resource = Resource(relevant_path, Resource.FILE)
    if update:
        curr = relevant_resource.get_data()
        curr.update(relevant_terms)
        relevant_resource.write_data(json.dumps(curr))
    else:
        relevant_resource.write_data(json.dumps(relevant_terms))


def write_cluster_score_vs_size(model, doc_size):
    """
    Write new scores and doc_size to file.
    NOTE: This will override the previous data
    @model: ClusteringModel instance
    @doc_size: Number of leads on which clustering was done
    """
    data = [(doc_size, model.silhouette_score)]
    path = model.get_cluster_data_path()
    data_path = os.path.join(path, settings.CLUSTER_SCORE_DOCS_SIZE_FILENAME)
    data_resource = Resource(data_path, Resource.FILE)
    data_resource.write_data(json.dumps(data))


def update_cluster_score_vs_size(model, increased_size=1):
    """
    Update scores. This won't override.
    @model: ClusteringModel isntance, this contains new score
    @increased_size
    """
    current_data = model.get_cluster_score_vs_size_data()
    last_size = current_data[-1][0]
    current_data.append((last_size+increased_size, model.silhouette_score))
    path = model.get_cluster_data_path()
    data_path = os.path.join(path, settings.CLUSTER_SCORE_DOCS_SIZE_FILENAME)
    data_resource = Resource(data_path, Resource.FILE)
    data_resource.write_data(json.dumps(current_data))


def write_clustered_data_to_files(
        model, docs_labels, cluster_centers,
        docids_features, update=False
        ):
    """Write the doc_clusterlabels and cluster_centers to files"""
    path = model.get_cluster_data_path()
    # create the directory
    p = subprocess.Popen(['mkdir', '-p', path], stdout=subprocess.PIPE)
    _, err = p.communicate()
    if err:
        print("Couldn't create cluster data files. {}".format(err))
        return

    # write centers data
    write_or_update_centers_data(model, cluster_centers)
    # write labels data
    write_cluster_labels_data(model, docs_labels, docids_features, update)
    print("Done writing data")
