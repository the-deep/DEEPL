import os
import json
import subprocess
import logging

from celery import task
from django.conf import settings
from django.utils import timezone

from clustering.models import ClusteringModel, Doc2VecModel
from clustering.base import ClusteringOptions
from clustering.kmeans_doc2vec import KMeansDoc2Vec
from clustering.kmeans_docs import KMeansDocs
from classifier.models import ClassifiedDocument
from classifier.tf_idf import get_relevant_terms
from helpers.utils import compress_sparse_vector, Resource
from helpers.common import preprocess, tokenize

logger = logging.getLogger(__name__)


@task
def create_new_clusters(
        name, group_id, n_clusters,
        CLUSTER_CLASS=KMeansDocs, doc2vec_group_id=None
        ):
    """If already exists, override it"""
    try:
        cluster_model = ClusteringModel.objects.get(group_id=group_id)
    except ClusteringModel.DoesNotExist:
        cluster_model = ClusteringModel.objects.create(
            name=name,
            group_id=group_id,
            n_clusters=n_clusters
        )
    return perform_clustering(cluster_model, CLUSTER_CLASS, doc2vec_group_id)


def write_clustered_data_to_files(
        model, docs_labels, cluster_centers,
        docids_features, relevant_terms=None, update=False
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
    # Center data can be directly written whether update is true or false as
    # centers gets updated
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
    # Write docs_clusterlabels
    if update:
        data = json.loads(labels_resource.get_data())
        data.update(dict_data)
        labels_resource.write_data(json.dumps(data))
    else:
        labels_resource.write_data(json.dumps(dict_data))
    # Write relevant terms if present
    if relevant_terms is not None:
        relevant_path = os.path.join(path, settings.RELEVANT_TERMS_FILENAME)
        relevant_resource = Resource(relevant_path, Resource.FILE)
        if update:
            data = set(json.loads(relevant_resource.get_data()))
            data = data.union(list(relevant_terms))
            relevant_resource.write_data(json.dumps(list(data)))
        else:
            relevant_resource.write_data(json.dumps(list(relevant_terms)))
    print("Done writing data")


@task
def recluster(group_id, num_clusters):
    try:
        cluster_model = ClusteringModel.objects.get(
            group_id=group_id,
            n_clusters=num_clusters
        )
        perform_clustering(cluster_model)
    except Exception as e:
        logger.warn("Exception while reclustering.  {}".format(e))


def perform_clustering(
        cluster_model, CLUSTER_CLASS=KMeansDocs, doc2vec_group_id=None
        ):
    n_clusters = cluster_model.n_clusters
    group_id = cluster_model.group_id
    name = cluster_model.name

    cluster_model.last_clustering_started = timezone.now()
    cluster_model.save()

    options = ClusteringOptions(n_clusters=n_clusters)
    if CLUSTER_CLASS == KMeansDocs:
        docs = ClassifiedDocument.objects.filter(group_id=group_id).\
                values('id', 'text')
        if not docs or docs.count() < n_clusters:
            logger.warn(
                "Too less documents for clustering for group_id {}".
                format(group_id)
            )
            raise Exception("Too less documents for given number of clusters")
        texts = list(
            map(
                lambda x: preprocess(x['text'], ignore_numbers=True),
                docs
            )
        )
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
    logger.info("Creating clustering model for group_id {}".format(group_id))
    kmeans_model = k_means.perform_cluster(cluster_params)
    docs_labels = zip(docids,  # convert from np.int64 to int
                      list(map(lambda x: int(x), kmeans_model.model.labels_)))

    # Save to database
    cluster_model.model = kmeans_model
    cluster_model.name = name
    cluster_model.group_id = group_id
    cluster_model.n_clusters = n_clusters
    logger.info("Saving model to database. Group_id".format(group_id))
    cluster_model.save()

    # create features for KMeansDocs
    if CLUSTER_CLASS == KMeansDocs:
        features = []
        vectorizer = kmeans_model.vectorizer
        for txt in texts:
            arr = vectorizer.transform([txt]).toarray()[0]
            compressed = compress_sparse_vector(arr)
            features.append(compressed)
        relevant_terms = get_relevant_terms(list(map(tokenize, texts)))

    docids_features = dict(zip(docids, features))
    # Now write to files
    logger.info(
        "Writing clustering results to files. Group id: {}".
        format(group_id)
    )
    write_clustered_data_to_files(
        cluster_model,
        docs_labels,
        kmeans_model.model.cluster_centers_,
        docids_features,
        relevant_terms
    )
    # mark clustering complete as true, and update clustered date
    cluster_model.ready = True
    cluster_model.silhouette_score = cluster_model.calculate_silhouette_score()
    cluster_model.last_clustered_on = timezone.now()
    cluster_model.save()
    return cluster_model


def get_unclustered_docs(cluster_model):
    """return docs dict with id and text"""
    # those documents are the ones which have same group_id and been added
    # after the last_cluster_started time
    filter_criteria = {
        'group_id': cluster_model.group_id
    }
    if cluster_model.last_clustering_started is not None:
        filter_criteria['created_on__gte'] = \
                cluster_model.last_clustering_started
    docs = ClassifiedDocument.objects.filter(**filter_criteria).\
        values('id', 'text')
    return docs


@task
def update_cluster(cluster_id):
    try:
        cluster_model = ClusteringModel.objects.get(id=cluster_id)
    except ClusteringModel.DoesNotExist:
        logger.warn("Clustering Model with id {} does not exist".format(
            cluster_id
        ))
    docs = get_unclustered_docs(cluster_model)
    texts = list(
            map(lambda x: preprocess(x['text'], ignore_numbers=True), docs)
        )
    docids = list(map(lambda x: x['id'], docs))
    kmeans_model = cluster_model.model
    CLUSTER_CLASS = type(kmeans_model)
    # TODO: add update criteria for doc2vec

    # update status
    cluster_model.ready = False
    cluster_model.last_clustering_started = timezone.now()
    cluster_model.save()

    kmeans_model.update_cluster(texts)
    docs_labels = list(zip(
        docids,  # convert from np.int64 to int
        list(map(lambda x: int(x), kmeans_model.model.labels_))
    ))
    if CLUSTER_CLASS == KMeansDocs:
        features = []
        vectorizer = kmeans_model.vectorizer
        for txt in texts:
            arr = vectorizer.transform([txt]).toarray()[0]
            compressed = compress_sparse_vector(arr)
            features.append(compressed)
        relevant_terms = get_relevant_terms(list(map(tokenize, texts)))
    # write/update to file
    docids_features = dict(zip(docids, features))
    write_clustered_data_to_files(
        cluster_model,
        docs_labels,
        kmeans_model.model.cluster_centers_,
        docids_features,
        relevant_terms,
        update=True
    )
    # update status
    cluster_model.last_clustered_on = timezone.now()
    cluster_model.silhouette_score = cluster_model.calculate_silhouette_score()
    cluster_model.ready = True
    cluster_model.save()


@task
def update_clusters():
    for clustermodel in ClusteringModel.objects.all().values('id'):
        update_cluster(clustermodel['id'])
