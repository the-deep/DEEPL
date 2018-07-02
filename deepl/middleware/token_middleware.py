import json
from django.http import HttpResponse

from api_auth.models import Token


class CheckTokenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args):
        if '/api/' in request.path and 'token' not in request.path:
            if not request.user.is_authenticated():
                token = request.META.get('HTTP_AUTHORIZATION')
                if not token:
                    return HttpResponse(
                        json.dumps(
                            {'message': 'Token not provided. Please provide token as API-Token header field.'}
                        ),
                        status=403,
                        content_type='application/json'
                    )
                    token = token.replace('Token ', '')
                try:
                    token = token.replace('Token ', '')
                    tokenobj = Token.objects.get(token=token)
                except Token.DoesNotExist:
                    return HttpResponse(
                        json.dumps({'message': 'Invalid token provided'}),
                        status=403,
                        content_type='application/json'
                    )
            else:
                # disable csrf checks
                setattr(request, '_dont_enforce_csrf_checks', True)
                # If user is authenticated, then use test token
                tokenobj = request.user.profile.tokens.filter(is_test=True)[0]
            # increment api_calls field of tokenobj
            tokenobj.api_calls += 1
            tokenobj.save()
        return self.get_response(request)
