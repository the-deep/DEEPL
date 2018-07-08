import json
from django.http import HttpResponse

from api_auth.models import Token


class CheckTokenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args):
        if '/api/' in request.path and 'token' not in request.path:
            token = request.META.get('HTTP_AUTHORIZATION')
            if not request.user.is_authenticated() and not token:
                # just let it pass, throttle will handle this
                return self.get_response(request)
            if token:
                try:
                    token = token.replace('Token ', '')
                    tokenobj = Token.objects.get(token=token)
                except Token.DoesNotExist:
                    return HttpResponse(
                        json.dumps({'message': 'Invalid token provided'}),
                        status=403,
                        content_type='application/json'
                    )
            elif request.user.is_authenticated():
                # disable csrf checks
                setattr(request, '_dont_enforce_csrf_checks', True)
                # If user is authenticated, then use test token
                tokenobj = request.user.profile.tokens.filter(is_test=True)[0]
            # increment api_calls field of tokenobj
            tokenobj.api_calls += 1
            tokenobj.save()
        return self.get_response(request)
