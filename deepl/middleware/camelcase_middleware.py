import json


class CamelCaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, **args):
        resp = self.get_response(request)

        case = request.GET.get('case', 'snakecase')
        if case == 'camelcase':
            return resp

        if hasattr(resp, 'data'):
            data = keys_to_camelcase(resp.data)
            resp.data = data
            resp.content = json.dumps(data)
        return resp


def keys_to_camelcase(data):
    if isinstance(data, list):
        return [keys_to_camelcase(x) for x in data]
    if not isinstance(data, dict):
        return data
    updated = {}
    for k, v in data.items():
        updated[snake_to_camel(k)] = keys_to_camelcase(v)
    return updated


def snake_to_camel(string):
    if not string:
        return string
    words = string.split('_')
    return words[0]+''.join([x.title() for x in words[1:]])
