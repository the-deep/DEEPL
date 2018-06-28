from rest_framework.test import APITestCase, APIClient


class BaseAPITestCase(APITestCase):

    def test_no_token(self):
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
