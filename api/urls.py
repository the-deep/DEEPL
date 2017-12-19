from django.conf.urls import url
from api.views import (
    DocumentClassifierView,
    TopicModelingView,
    KeywordsExtractionView,
    ApiVersionsView
)

urlpatterns = [
    url(r'^(?P<version>[a-z0-9A-Z\.]+)/classify/$', DocumentClassifierView.as_view()),
    url(r'topic-modeling/$', TopicModelingView.as_view()),
    url(r'versions/$', ApiVersionsView.as_view()),
    url(r'keywords-extraction/$', KeywordsExtractionView.as_view()),
]
