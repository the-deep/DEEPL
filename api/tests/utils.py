from rest_framework.test import APIClient

from api_auth.models import Token


def with_token_auth_tests(cls):
    """
    This decorator adds test_no_token method to the class and
    modifies setup method
    """
    class newclass(cls):
        def setUp(self):
            super().setUp()
            # create a token
            self.token = Token.objects.create()
            self.client.credentials(
                HTTP_AUTHORIZATION='Token ' + str(self.token.token)
            )

        # this is not used
        def no_test_test_no_token(self):
            client = APIClient()
            # if not attribute called api_url do nothing
            if not hasattr(self, 'api_url'):
                return
            # try post
            response = client.post(self.api_url, {})
            if not response.status_code == 405:
                assert response.status_code == 403
            # try get
            response = client.get(self.api_url, {})
            if not response.status_code == 405:
                assert response.status_code == 403
            # try put
            response = client.put(self.api_url, {})
            if not response.status_code == 405:
                assert response.status_code == 403
    return newclass
