from django.conf.urls import url
from core.views import HomePageView

urlpatterns = [
    url(r'^', HomePageView.as_view()),
]
