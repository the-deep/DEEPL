from django.conf.urls import url
from api.views import (
    DocumentClassifierView,
    TopicModelingView,
    KeywordsExtractionView,
    ApiVersionsView,
    RecommendationView,
    NERView,
    NERWithDocIdView,
    CorrelationView,
    DocsSimilarityView,
    SimilarDocsView,
    ClusteringView,
)

urlpatterns = [
    url(
        r'^(?P<version>[a-z0-9A-Z\.]+)/classify/$',
        DocumentClassifierView.as_view()
    ),
    url(r'topic-modeling/$', TopicModelingView.as_view()),
    url(r'ner/$', NERView.as_view()),
    url(r'ner-docs/$', NERWithDocIdView.as_view()),
    url(r'versions/$', ApiVersionsView.as_view()),
    url(r'keywords-extraction/$', KeywordsExtractionView.as_view()),
    url(
        r'^(?P<version>[a-z0-9A-Z\.]+)/recommendation/$',
        RecommendationView.as_view()
    ),
    url(r'^(?P<entity>[a-zA-Z\.]+)/correlation/$', CorrelationView.as_view()),
    url(r'^similarity/$', DocsSimilarityView.as_view()),
    url(r'^similardocs/$', SimilarDocsView.as_view()),
    url(r'^clustering/$', ClusteringView.as_view())
]
