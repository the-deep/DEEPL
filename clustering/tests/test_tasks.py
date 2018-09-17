import os

from rest_framework.test import APITestCase
from django.conf import settings

from classifier.models import ClassifiedDocument
from clustering.models import ClusteringModel
from clustering.tasks import (
    create_new_clusters,
    recluster,
    update_clusters,
    get_unclustered_docs,
    assign_cluster_to_doc
)


class TestCreateClusters(APITestCase):
    """
    Test for clustering.tasks.create_new_clusters() function
    - will also test clustering.tasks.write_clustered_data_to_files
    """
    fixtures = [
        'fixtures/classifier.json',
        'fixtures/test_base_models.json',
        'fixtures/test_classified_docs.json'
    ]

    def setUp(self):
        # create dir
        self.test_cluster_data_dir = '/test_cluster_data'
        os.system('mkdir -p {}'.format(self.test_cluster_data_dir))

        os.environ[settings.ENVIRON_CLUSTERING_DATA_LOCATION] = \
            self.test_cluster_data_dir
        self.doc_sample = ClassifiedDocument.objects.last()
        self.group_id = self.doc_sample.group_id
        self.n_clusters = 2
        self.cluster_name = "test cluster"

    def test_new_cluster_created(self):
        assert ClusteringModel.objects.all().count() == 0
        create_new_clusters(self.cluster_name, self.group_id, self.n_clusters)
        assert ClusteringModel.objects.all().count() == 1
        model = ClusteringModel.objects.last()
        assert model.group_id == self.group_id
        assert model.ready
        # test appropriate files created
        dirname = os.path.join(
            self.test_cluster_data_dir,
            "cluster_model_{}".format(model.id)
        )
        assert os.path.isdir(dirname)
        # also check size vs cluster score file created
        data = model.get_cluster_score_vs_size_data()
        assert data is not None
        assert data != []
        assert isinstance(data, list)

    def test_recluster(self):
        # first remove all existing clusters
        ClusteringModel.objects.all().delete()
        # and then create a new cluster
        create_new_clusters(self.cluster_name, self.group_id, self.n_clusters)
        assert ClusteringModel.objects.all().count() == 1
        model = ClusteringModel.objects.last()
        recluster(model)
        newmodel = ClusteringModel.objects.last()
        assert newmodel.ready
        assert newmodel.last_clustering_started > model.last_clustering_started
        assert newmodel.last_clustered_on > model.last_clustered_on
        # also check size vs cluster score file created
        data = model.get_cluster_score_vs_size_data()
        assert data is not None
        assert data != []
        assert isinstance(data, list)

    def test_update_cluster(self):
        # first remove all existing clusters
        ClusteringModel.objects.all().delete()
        # and then create a new cluster
        create_new_clusters(self.cluster_name, self.group_id, self.n_clusters)
        assert ClusteringModel.objects.all().count() == 1
        model = ClusteringModel.objects.last()
        # add new classifiedDocument
        ClassifiedDocument.objects.create(
            classifier=self.doc_sample.classifier,
            group_id=self.doc_sample.group_id,
            text="This is another text",
            classification_label="dummy_label"
        )
        labels_data = model.get_labels_data()
        len_docs = len(labels_data.keys())
        unclustered = get_unclustered_docs(model)
        assert unclustered, "There should be 1 unclustered doc"
        # get current score_vs size data
        old_data = model.get_cluster_score_vs_size_data()

        update_clusters()

        # get new clustere score vs size data
        new_data = model.get_cluster_score_vs_size_data()
        assert len(old_data) + 1 == len(new_data)
        assert new_data[-2] == old_data[-1]

        newmodel = ClusteringModel.objects.last()
        labels_data = newmodel.get_labels_data()
        newlen_docs = len(labels_data.keys())
        # also check number of docs has increased. Read from file
        assert newlen_docs == len_docs + 1, "Since one doc is added"

        assert newmodel.ready
        assert newmodel.last_clustering_started > model.last_clustering_started
        assert newmodel.last_clustered_on > model.last_clustered_on

    def test_assign_cluster_to_doc(self):
        # first remove all existing clusters
        ClusteringModel.objects.all().delete()
        # and then create a new cluster
        create_new_clusters(self.cluster_name, self.group_id, self.n_clusters)
        assert ClusteringModel.objects.all().count() == 1
        model = ClusteringModel.objects.last()
        # add new classifiedDocument
        doc = ClassifiedDocument.objects.create(
            classifier=self.doc_sample.classifier,
            group_id=self.doc_sample.group_id,
            text="This is another text",
            classification_label="dummy_label"
        )
        labels_data = model.get_labels_data()
        len_docs = len(labels_data.keys())
        unclustered = get_unclustered_docs(model)
        assert unclustered, "There should be 1 unclustered doc"

        assign_cluster_to_doc(doc.id)

        newmodel = ClusteringModel.objects.last()
        labels_data = newmodel.get_labels_data()
        newlen_docs = len(labels_data.keys())
        # also check number of docs has increased. Read from file
        assert newlen_docs == len_docs + 1, "Since one doc is added"
        assert newmodel.ready

    def tearDown(self):
        # remove created dirs
        os.system('rm -r {}'.format(self.test_cluster_data_dir))
