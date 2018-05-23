import unittest
import os
import json
from django.conf import settings
from rest_framework.test import APITestCase

from classifier.models import ClassifiedDocument
from clustering.base import ClusteringOptions
from clustering.kmeans_docs import KMeansDocs
from clustering.tasks import create_new_clusters
from helpers.utils import Resource


class TestKMeansDocs(unittest.TestCase):
    def setUp(self):
        self.documents = [
            "this is a test document that is to be tested for various NLP algorithms.",  # noqa
            "document classification and clustering is a very important task in NLP", # noqa
            "Computers are these days almost as important as electricity",
            "Not only computers are important, they are part of life as well"
        ]
        self.clustering_options = ClusteringOptions(n_clusters=2)

    def test_creation_kmeans_docs(self):
        kmeansdocs = KMeansDocs(self.clustering_options)
        km = kmeansdocs.perform_cluster(self.documents)
        assert km == kmeansdocs
        assert km.X is not None
        sc = km.get_silhouette_score()
        assert sc >= -1 and sc <= 1


class TestClusterCreationDocs(APITestCase):
    fixtures = [
        'fixtures/classifier.json',
        'fixtures/test_base_models.json',
        'fixtures/test_classified_docs.json'
    ]

    def setUp(self):
        # choose random group_id from database
        self.group_id = ClassifiedDocument.objects.last().group_id
        self.cluster_data_path = 'test_clusters/'
        # create path if not exist
        os.system('mkdir -p {}'.format(self.cluster_data_path))
        os.environ[settings.ENVIRON_CLUSTERING_DATA_LOCATION] = \
            self.cluster_data_path

    def test_data_files_created(self):
        model = create_new_clusters('test', self.group_id, 2)
        path = self.get_model_path(model)
        center_path = os.path.join(path, settings.CLUSTERS_CENTERS_FILENAME)
        labels_path = os.path.join(
            path,
            settings.CLUSTERED_DOCS_LABELS_FILENAME
        )
        relevant_path = os.path.join(path, settings.RELEVANT_TERMS_FILENAME)
        size_score_path = os.path.join(
            path, settings.CLUSTER_SCORE_DOCS_SIZE_FILENAME
        )
        center_resource = Resource(center_path, Resource.FILE)
        labels_resource = Resource(labels_path, Resource.FILE)
        relevant_resource = Resource(relevant_path, Resource.FILE)
        size_score_resource = Resource(size_score_path, Resource.FILE)
        # check centers
        try:
            center_resource.validate()
        except Exception as e:
            assert False, "No center data stored. " + e.args
        else:
            data = json.loads(center_resource.get_data())
            assert isinstance(data, dict)
        # check labels
        try:
            labels_resource.validate()
        except Exception as e:
            assert False, "No levels data stored. " + e.args
        else:
            data = json.loads(labels_resource.get_data())
            assert isinstance(data, dict)
        # check relevant
        try:
            relevant_resource.validate()
        except Exception as e:
            assert False, "No relevant data stored. " + e.args
        else:
            data = json.loads(relevant_resource.get_data())
            assert isinstance(data, dict)
            for k, v in data.items():
                assert isinstance(v, list)
        # check size vs score
        try:
            size_score_resource.validate()
        except Exception as e:
            assert False, "No score data stored. " + e.args
        else:
            data = json.loads(size_score_resource.get_data())
            assert isinstance(data, list)
            for x in data:
                assert isinstance(x, list)
                assert len(x) == 2

    def get_model_path(self, model):
        cluster_data_location = settings.ENVIRON_CLUSTERING_DATA_LOCATION
        resource = Resource(
            cluster_data_location,
            Resource.FILE_AND_ENVIRONMENT
        )
        path = os.path.join(
            resource.get_resource_location(),
            'cluster_model_{}'.format(model.id)
        )
        return path

    def tearDown(self):
        # remove test cluster folder
        os.system('rm -r {}'.format(self.cluster_data_path))
