from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class TokenView(APIView):
    """API for getting tokens"""
    def get(self, request, version=None):
        if not request.user.is_authenticated():
            return Response(
                {'message': 'Please Login'},
                status=status.HTTP_403_FORBIDDEN
            )
        profile = request.user.profile
        if not profile:
            return Response(
                {'message': 'No profile found, are you a normal api user?'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {'test_token': profile.test_token, 'api_token': profile.api_token}
        )
