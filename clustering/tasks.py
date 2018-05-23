import logging

from celery import task
from django.utils import timezone

from clustering.models import ClusteringModel, Doc2VecModel
from clustering.base import ClusteringOptions
from clustering.kmeans_doc2vec import KMeansDoc2Vec
from clustering.kmeans_docs import KMeansDocs
from clustering.helpers import (
    write_clustered_data_to_files,
    write_cluster_labels_data,
    write_cluster_score_vs_size,
    update_cluster_score_vs_size,
    write_relevant_terms_data,
)
from classifier.models import ClassifiedDocument
from helpers.utils import compress_sparse_vector
from helpers.common import preprocess

logger = logging.getLogger('celery')


def create_new_clusters(
        name, group_id, n_clusters,
        CLUSTER_CLASS=KMeansDocs, doc2vec_group_id=None
        ):
    try:
        cluster_model = ClusteringModel.objects.get(group_id=group_id)
    except ClusteringModel.DoesNotExist:
        cluster_model = ClusteringModel.objects.create(
            name=name,
            group_id=group_id,
            n_clusters=n_clusters
        )
    updated_model = perform_clustering(
        cluster_model, CLUSTER_CLASS, doc2vec_group_id
    )
    # create score_vs_size
    size = ClassifiedDocument.objects.filter(group_id=group_id).count()
    write_cluster_score_vs_size(updated_model, size)
    return updated_model


@task
def create_new_clusters_task(*args, **kwargs):
    create_new_clusters(*args, **kwargs)
    return True


@task
def recluster(group_id, num_clusters):
    try:
        cluster_model = ClusteringModel.objects.get(
            group_id=group_id,
            n_clusters=num_clusters
        )
        updated_model = perform_clustering(cluster_model)
        size = ClassifiedDocument.objects.filter(group_id=group_id).count()
        write_clustered_data_to_files(updated_model, size)
        return True
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
        docids_features
    )
    # relevant terms can be calculated only after writing other data
    relevant_terms = cluster_model.compute_relevant_terms()
    write_relevant_terms_data(cluster_model, relevant_terms)

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
    increased_size = docs.count()
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
    # write/update to file
    docids_features = dict(zip(docids, features))
    write_clustered_data_to_files(
        cluster_model,
        docs_labels,
        kmeans_model.model.cluster_centers_,
        docids_features,
        update=True
    )
    # relevant terms can be calculated only after writing other data
    relevant_terms = cluster_model.compute_relevant_terms()
    write_relevant_terms_data(cluster_model, relevant_terms)

    # update status
    cluster_model.last_clustered_on = timezone.now()
    cluster_model.silhouette_score = cluster_model.calculate_silhouette_score()
    cluster_model.ready = True
    cluster_model.save()
    # Update size vs silhouette scores
    update_cluster_score_vs_size(cluster_model, increased_size)


@task
def update_clusters():
    for clustermodel in ClusteringModel.objects.all().values('id'):
        update_cluster(clustermodel['id'])


@task
def assign_cluster_to_doc(doc_id):
    doc = ClassifiedDocument.objects.get(id=doc_id)
    grp_id = doc.group_id
    cluster_model = ClusteringModel.objects.get(group_id=grp_id)
    model = cluster_model.model  # instance of KMeansDocs class
    processed = preprocess(doc.text)
    X = model.vectorizer.transform([processed]).toarray()[0]
    label = int(model.model.predict([X])[0])
    docs_labels = [(doc_id, label)]
    feature = compress_sparse_vector(list(map(lambda x: float(x), X)))
    features = {doc_id: feature}
    # update labels data
    write_cluster_labels_data(
        cluster_model, docs_labels, features, update=True
    )
    # calculate new silhouette score
    silhouette_score = cluster_model.calculate_silhouette_score()
    cluster_model.silhouette_score = silhouette_score
    cluster_model.save()
    # update_size vs silhouette scores
    update_cluster_score_vs_size(cluster_model, 1)  # increased size is 1
    # TODO: if silhouette score reaches below a threshold, rerun clusters
