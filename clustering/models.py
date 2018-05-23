import pickle
import os
import json
from gensim.models.doc2vec import Doc2Vec


from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings

from classifier.models import BaseModel
from helpers.utils import Resource, uncompress_compressed_vector, distance
from .helpers import write_relevant_terms_data


class ClusteringModel(BaseModel):
    """
    Model to store clustering data
    """
    # TODO: might need to maintain history of clusters
    name = models.CharField(max_length=100)
    group_id = models.CharField(max_length=20, unique=True, editable=False)
    _data = models.BinaryField()
    n_clusters = models.IntegerField()
    extra_info = JSONField(default={})
    silhouette_score = models.FloatField(default=-1.0)
    last_clustering_started = models.DateTimeField(null=True)
    # when clustering was completed
    last_clustered_on = models.DateTimeField(null=True)
    ready = models.BooleanField(default=False)

    def set_model(self, modelobj):
        self._data = pickle.dumps(modelobj)

    def get_model(self):
        return pickle.loads(self._data)

    model = property(get_model, set_model)

    def __str__(self):
        return "{} - Group {}".format(self.name, self.group_id)

    def get_centers_data(self):
        path = self.get_cluster_data_path()
        centers_path = os.path.join(
            path, settings.CLUSTERS_CENTERS_FILENAME
        )
        labels_resource = Resource(centers_path, Resource.FILE)
        data = json.loads(labels_resource.get_data())
        return data

    def get_cluster_score_vs_size_data(self):
        path = self.get_cluster_data_path()
        data_path = os.path.join(
            path, settings.CLUSTER_SCORE_DOCS_SIZE_FILENAME
        )
        data_resource = Resource(data_path, Resource.FILE)
        datastr = data_resource.get_data()
        if datastr is None:
            return []
        return json.loads(datastr)

    def get_labels_data(self):
        path = self.get_cluster_data_path()
        labels_path = os.path.join(
            path, settings.CLUSTERED_DOCS_LABELS_FILENAME
        )
        labels_resource = Resource(labels_path, Resource.FILE)
        data = json.loads(labels_resource.get_data())
        return data

    def get_cluster_data_path(self):
        resource = self.get_cluster_data_resource()
        # create another resource(folder to keep files)
        path = os.path.join(
            resource.get_resource_location(),
            'cluster_model_{}'.format(self.id)
        )
        return path

    @staticmethod
    def get_cluster_data_resource():
        cluster_data_location = settings.ENVIRON_CLUSTERING_DATA_LOCATION
        return Resource(
            cluster_data_location,
            Resource.FILE_AND_ENVIRONMENT
        )

    def get_doc_label(self, docid, labeldata=None):
        if labeldata is None:
            labeldata = self.get_labels_data()
        if not labeldata.get(docid):
            return None
        return labeldata[docid]['label']

    def get_similar_docs_for_label(self, label):
        data = self.get_labels_data()
        similar_docs = []
        for k, v in data.items():
            if v['label'] == label:
                similar_docs.append(k)
        return similar_docs

    def get_similar_docs(self, doc_id):
        data = self.get_labels_data()
        doc_label = self.get_doc_label(doc_id, data)
        if doc_label is None:
            # TODO: more informative
            return []
        return self.get_similar_docs_for_label(doc_label)

    def get_relevant_terms_data(self):
        """This gets data from file unlike compute_relevant terms,
        which calculates relevant terms"""
        path = self.get_cluster_data_path()
        data_path = os.path.join(
            path, settings.RELEVANT_TERMS_FILENAME
        )
        data_resource = Resource(data_path, Resource.FILE)
        raw = data_resource.get_data()
        if not raw:
            return json.loads(raw)
        # compute and write to file
        data = self.compute_relevant_terms()
        # Write to file
        write_relevant_terms_data(self, data)
        return data

    def compute_relevant_terms(self):
        km = self.model.model
        vectorizer = self.model.vectorizer
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        clusters_terms = {}
        for i in range(self.n_clusters):
            clusters_terms[i] = []
            for ind in order_centroids[i, :10]:  # NOTE: 10 terms per cluster
                clusters_terms[i].append(terms[ind])
        return clusters_terms

    def calculate_silhouette_score(self):
        """Calculate silhouette score for clusters"""
        # NOTE/TODO: only for tf-idf now, not for doc2vec
        # FORMULA: (b - a) / max (a, b)
        # where b = minimal dist of point from all other cluster centroids
        # a = dist from point to its own cluster centroid
        labels_data = self.get_labels_data()
        centers_data = self.get_centers_data()
        same_cluster_avg_dist = 0  # A
        diff_cluster_avg_dist = 0  # B
        total_docs = len(labels_data.keys())
        for k, v in labels_data.items():
            a = 9999999
            b = 9999999  # is the minimal distance
            label_vector = uncompress_compressed_vector(v['features'])
            for c, vec in centers_data.items():
                center_vec = uncompress_compressed_vector(vec)
                dist = distance(label_vector, center_vec)
                if c == v['label']:
                    a = dist
                elif dist < b:
                    b = dist
            same_cluster_avg_dist += a
            diff_cluster_avg_dist += b
        B, A = diff_cluster_avg_dist, same_cluster_avg_dist
        score = (B - A) / max(A, B)
        return float(score)/float(total_docs)


class Doc2VecModel(BaseModel):
    """
    Model to store data about gensim doc2vec model created
    """
    name = models.CharField(max_length=100)
    group_id = models.CharField(max_length=20, unique=True, editable=False)
    modelpath = models.CharField(max_length=500)

    PATHTYPE_FILE = 'FILE'
    PATHTYPE_URL = 'URL'

    PATHTYPE_CHOICES = (
        (PATHTYPE_FILE, 'File'),
        (PATHTYPE_URL, 'Url')
    )

    pathtype = models.CharField(
        max_length=50,
        choices=PATHTYPE_CHOICES,
        default=PATHTYPE_FILE
    )

    extra_info = JSONField(default={})

    @classmethod
    def new(cls, doc2vecmodel, name, group_id, extra_info={}):
        resource = Resource(
            settings.ENVIRON_DOC2VEC_MODELS_LOCATION,
            Resource.DIRECTORY_AND_ENVIRONMENT
        )
        path = resource.get_resource_location()
        doc2vec = cls(
            name=name,
            group_id=group_id,
            modelpath=path,
            extra_info=extra_info
        )
        doc2vec.save()
        filename = 'doc2vec_id_{}'.format(doc2vec.id)
        doc2vec.modelpath = os.path.join(doc2vec.modelpath, filename)
        doc2vec.save()
        # finally save the doc2vec model in a file
        doc2vecmodel.save(doc2vec.modelpath)
        return doc2vec

    @property
    def model(self):
        return Doc2Vec.load(self.modelpath)
