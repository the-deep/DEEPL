from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response

from fuzzy.levenshtein import find_matching


import logging
logger = logging.getLogger('django')


class FuzzySearchView(APIView):
    """
    API for fuzzy searching
    """
    valid_types = ['country']

    def get(self, request, version=None, type='country'):
        if type not in self.valid_types:
            return Response(
                {'message': 'No fuzzy search for {}.'.format(type)},
                status=status.HTTP_404_NOT_FOUND
            )

        data = dict(request.query_params.items())
        self.validate(data)

        return Response({
            'matches': find_matching(data['query'], type)
        })

    def validate(self, data):
        errors = {}
        rawquery = data.get('query') or ''
        query = ' '.join(rawquery.split())
        if len(query) < 3:
            errors['query'] = 'query should not be empty and be at least 3 characters long.'  # noqa
        if errors:
            raise exceptions.ValidationError(errors)
