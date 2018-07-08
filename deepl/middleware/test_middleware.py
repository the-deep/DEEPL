import json


class TestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args):
        pass
