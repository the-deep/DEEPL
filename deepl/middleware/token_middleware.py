import re
import json
from django.conf import settings
from django.http import HttpResponse
from importlib import import_module

from api_auth.models import Token

import logging
logger = logging.getLogger(__name__)


class CheckTokenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args):
        if '/api/' in request.path and 'token' not in request.path:
            token = request.META.get('HTTP_AUTHORIZATION')
            # Check if coming from localhost. If so, send static response
            host = request.META.get('HTTP_HOST', '')
            if settings.DEBUG and 'localhost' in host:
                response = get_static_response(request)
                if response is None:
                    return HttpResponse(
                        json.dumps(
                            {'message': 'No static response for this url.'}
                        ),
                        status=410,  # 410 GONE
                        content_type='application/json'
                    )
                else:
                    return HttpResponse(
                        json.dumps(response),
                        content_type='application/json'
                    )
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


def get_static_response(request):
    url = request.path
    m = re.match('/api/(v\d+/|)(.*)', url)
    action = m.group(2)
    # replace back slash
    if action[-1] == '/':
        action = action[:-1]
    action = action.replace('-', '_')
    try:
        module = import_module('static_responses.{}'.format(action))
        if hasattr(module, 'static_data'):
            data = module.static_data()
            return data
        else:
            logger.warn("Module for static response found but no method static_data()")
    except ImportError:
        print("no module for static response found")
        return None
    return None
