from django.conf.urls import url
from api.views import DocumentClassifierView, TopicModelingView

urlpatterns = [
    url(r'^classify/$', DocumentClassifierView.as_view()),
    url(r'^topic-modeling/$', TopicModelingView.as_view()),
]
