from django.conf.urls import url
from api.views import DocumentClassifierView, TopicModelingView

urlpatterns = [
    url(r'^(?P<version>[a-z0-9A-Z\.]+)/classify/$', DocumentClassifierView.as_view()),
    url(r'topic-modeling/$', TopicModelingView.as_view()),
]
