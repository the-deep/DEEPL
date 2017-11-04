from django.conf.urls import url
from api.views import DocumentClassifierView

urlpatterns = [
    url(r'^classify/$', DocumentClassifierView.as_view()),
]
