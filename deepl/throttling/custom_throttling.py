from rest_framework.throttling import SimpleRateThrottle
from django.conf import settings

from api_auth.models import Token


class DemoUserRateThrottle(SimpleRateThrottle):
    scope = 'anon'

    def get_cache_key(self, request, view):
        if '/api/' not in request.path:
            return None
        # if authenticated or has valid token, let it pass by returning None
        token = request.META.get('HTTP_AUTHORIZATION')
        if request.user.is_authenticated() or \
                (token and Token.objects.filter(
                    token=token.replace('Token ', '')
                    ).exists()):
            return None
        return request.path
