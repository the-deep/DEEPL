from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from clustering.models import ClusteringModel
from clustering.serializers import ClusteringModelSerializer
from clustering.tasks import create_clusters_task, recluster
from classifier.models import ClassifiedDocument


import logging
logger = logging.getLogger(__name__)


class ClusteringView(APIView):
    """
    API for document clusters
    """
    def get(self, request, version=None):
        data = dict(request.query_params.items())
        validation_details = self._validate_get_data(data)
        if not validation_details['status']:
            return Response(
                validation_details['errors'],
                status=status.HTTP_400_BAD_REQUEST
            )
        model_id = data['cluster_model_id']
        try:
            cluster_model = ClusteringModel.objects.get(id=model_id)
        except ClusteringModel.DoesNotExist:
            return Response(
                {
                    'message':
                    'Clustering model corresponding to model id does not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ClusteringModelSerializer(cluster_model)
        return Response(serializer.data)

    def post(self, request, version=None):
        data = dict(request.data.items())
        validation_details = self._validate_post_data(data)
        if not validation_details['status']:
            return Response(
                validation_details['errors'],
                status=status.HTTP_400_BAD_REQUEST
            )
        grp_id = data['group_id']
        num_clusters = int(data['num_clusters'])
        # first try get if any docs available with given group_id

        docs = ClassifiedDocument.objects.filter(group_id=grp_id)
        if not docs or docs.count() <= num_clusters:
            return Response(
                {'message': 'Too few/zero documents to cluster'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            cluster_model = ClusteringModel.objects.get(
                group_id=grp_id,
                n_clusters=num_clusters
            )
        except ClusteringModel.DoesNotExist:
            # TODO: find optimal clusters
            cluster_model = ClusteringModel.objects.create(
                group_id=grp_id,
                name=data.get('name', grp_id),  # name is not mandatory
                n_clusters=num_clusters
            )
            create_clusters_task.delay(
                cluster_model.id
            )
            return Response(
                {
                    "message": "Clustering is in progress. Use cluster_model_id for data",  # noqa
                    "cluster_model_id": cluster_model.id
                },
                status=status.HTTP_202_ACCEPTED
            )
        if not cluster_model.ready:
            return Response(
                {
                    "message": "Clustering is in progress. Try later for data.",  # noqa
                    "cluster_model_id": cluster_model.id
                },
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            {'cluster_model_id': cluster_model.id},
            status=status.HTTP_201_CREATED
        )

    def _validate_post_data(self, data):
        errors = {}
        if not data.get('group_id'):
            errors['group_id'] = 'Group id should be present'
        num_clusters = data.get('num_clusters')
        try:
            n = int(num_clusters)
            if n < 0:
                raise ValueError
        except (ValueError, TypeError):
            errors['num_clusters'] = 'num_clusters should be an integer'
        if errors:
            return {
                'status': False,
                'errors': errors
            }
        return {
            'status': True,
            'data': data
        }

    def _validate_get_data(self, data):
        errors = {}
        model_id = data.get('cluster_model_id')
        if not model_id:
            errors['cluster_model_id'] = "cluster_model_id should be present"
        else:
            try:
                i = int(model_id)
                if i < 0:
                    raise ValueError
            except (ValueError, TypeError):
                errors['cluster_model_id'] = 'cluster_model_id should be positive integer'
        if errors:
            return {
                'status': False,
                'errors': errors
            }
        return {
            'status': True,
            'data': data
        }


class ReClusteringView(APIView):
    """
    Re-Cluster api
    """
    def post(self, request, version=None):
        data = dict(request.data.items())
        validation_details = validate_post_recluster_data(data)
        if not validation_details['status']:
            return Response(
                validation_details['errors'],
                status=status.HTTP_400_BAD_REQUEST
            )
        grp_id = data['group_id']
        num_clusters = int(data['num_clusters'])
        try:
            cluster_model = ClusteringModel.objects.get(
                group_id=grp_id,
                n_clusters=num_clusters
            )
        except ClusteringModel.DoesNotExist:
            return Response(
                {'message': 'The corresponding cluster model does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not cluster_model.ready:
            return Response(
                {'message': 'The model is not ready. Try later'},
                status=status.HTTP_202_ACCEPTED
            )
        # now call to do reclustering
        cluster_model.ready = False
        cluster_model.save()
        recluster.delay(grp_id, num_clusters)
        return Response(
            {'message': 'Reclustering in progress.'},
            status=status.HTTP_202_ACCEPTED
        )


class ClusteringDataView(APIView):
    def get(self, request, version=None):
        data = dict(request.query_params.items())
        validation_details = self._validate_get_data(data)
        if not validation_details['status']:
            return Response(
                validation_details['errors'],
                status=status.HTTP_400_BAD_REQUEST
            )
        model_id = data['cluster_model_id']
        # now get cluster
        try:
            cluster_model = ClusteringModel.objects.get(id=model_id)
        except ClusteringModel.DoesNotExist:
            return Response(
                {'message': 'No such cluster found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not cluster_model.ready:
            return Response(
                {'message': 'Clustering in progress. Try again laer'},
                status=status.HTTP_202_ACCEPTED
            )
        data = cluster_model.get_relevant_terms_data()
        cluster_format_data = []
        for k, v in data.items():
            size = len(v)
            for i, e in enumerate(v):
                cluster_format_data.append(
                    {'cluster': k, 'score': size-i, 'value': e}
                )
        return Response({'data': cluster_format_data})

    def _validate_get_data(self, data):
        errors = {}
        if not data.get('cluster_model_id'):
            errors['cluster_model_id'] = 'cluster_model_id not provided'
        if errors:
            return {
                'status': False,
                'errors': errors
            }
        return {
            'status': True,
            'data': data
        }


def validate_post_recluster_data(data):
    errors = {}
    if not data.get('group_id'):
        errors['group_id'] = 'group_id should be present'
    num_clusters = data.get('num_clusters')
    try:
        v = int(num_clusters)
        if v < 0:
            raise ValueError
    except (ValueError, TypeError):
        errors['num_clusters'] = 'num_clusters should be present and positive int'  # noqa
    if errors:
        return {
            'status': False,
            'errors': errors
        }
    return {
        'status': True,
        'data': data
    }
