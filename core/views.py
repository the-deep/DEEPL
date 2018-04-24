from django.shortcuts import render
from rest_framework.views import APIView

import logging
logger = logging.getLogger(__name__)


class HomePageView(APIView):
    def get(self, request):
        return render(request, 'base.html', {})
