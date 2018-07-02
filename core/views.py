from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from rest_framework.views import APIView

from api_auth.serializers import UserSerializer

import logging
logger = logging.getLogger(__name__)


class HomePageView(APIView):
    def get(self, request):
        user = request.user
        if not user.is_authenticated():
            return redirect('/login')
        return render(request, 'main.html', {})


class LoginView(View):
    def get(self, request, context={}):
        if request.user.is_authenticated():
            return redirect('/')
        return render(request, 'login.html', context)

    def post(self, request):
        postdata = request.POST
        user = authenticate(
            username=postdata.get('username'),
            password=postdata.get('password')
        )
        if not user:
            logger.info("not authenticated")
            return self.get(request, {'message': 'Invalid credentials'})
        else:
            login(request, user)
            return redirect('/')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect('/')
        return render(request, 'register.html', {})

    def post(self, request):
        userdata = request.POST
        serializer = UserSerializer(userdata)
        serializer.create()


def user_logout(request):
    logout(request)
    return redirect('/login')
