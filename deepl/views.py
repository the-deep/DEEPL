from django.views import View
from django.contrib.auth import authenticate


class LoginView(View):
    def post(self, request):
        postdata = request.data()
        user = authenticate(
            username=postdata.get('username'),
            password=postdata.get('password')
        )
        if not user:
            pass
