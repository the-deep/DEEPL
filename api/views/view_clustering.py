from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from clustering.models import ClusteringModel
from clustering.tasks import create_new_clusters


import logging
logger = logging.getLogger(__name__)


class ClusteringView(APIView):
    """
    API for document clusters
    """
    def post(self, request, version=None):
        data = dict(request.data.items())
        validation_details = self._validate_data(data)
        if not validation_details['status']:
            return Response(
                validation_details,
                status=status.HTTP_400_BAD_REQUEST
            )
        grp_id = data['group_id']
        try:
            cluster_model = ClusteringModel.objects.get(
                group_id=grp_id
            )
        except ClusteringModel.DoesNotExist:
            # TODO: find optimal clusters
            cluster_model = create_new_clusters.delay(
                data.get('name', grp_id),  # name is not mandatory
                grp_id,
                n_clusters=int(data['num_clusters']),
            )
            return Response(
                {"message": "Clustering is in progress. Try later for data."},
                status=status.HTTP_202_ACCEPTED
            )
        if not cluster_model.ready:
            return Response(
                {"message": "Clustering is in progress. Try later for data."},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            {'cluster_id': cluster_model.id},
            status=status.HTTP_201_CREATED
        )

    def _validate_data(self, data):
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
