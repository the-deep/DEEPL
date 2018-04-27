import os
import json

from rest_framework import serializers
from django.conf import settings

from clustering.models import ClusteringModel
from classifier.models import ClassifiedDocument
from helpers.utils import Resource


class ClusteringModelSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    doc_ids = serializers.SerializerMethodField()
    relevant_terms = serializers.SerializerMethodField()

    class Meta:
        model = ClusteringModel
        fields = (
            'id', 'group_id', 'n_clusters',
            'score', 'doc_ids', 'relevant_terms'
        )

    def get_score(self, obj):
        return obj.silhouette_score

    def get_doc_ids(self, obj):
        docs = ClassifiedDocument.objects.filter(group_id=obj.group_id).\
            values('id')
        return [x['id'] for x in docs]

    def get_relevant_terms(self, obj):
        cluster_data_location = settings.ENVIRON_CLUSTERING_DATA_LOCATION
        resource = Resource(
            cluster_data_location,
            Resource.FILE_AND_ENVIRONMENT
        )
        path = os.path.join(
            resource.get_resource_location(),
            'cluster_model_{}'.format(obj.id)
        )
        relevant_path = os.path.join(path, settings.RELEVANT_TERMS_FILENAME)
        relevant_resource = Resource(relevant_path, Resource.FILE)
        return json.loads(relevant_resource.get_data())
