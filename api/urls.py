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
    ClusteringDataView,
    ReClusteringView,
    ClassifiedDocumentView,
    TokenView
)

urlpatterns = [
    url(r'^classify/$', DocumentClassifierView.as_view()),
    url(r'^topic-modeling/$', TopicModelingView.as_view()),
    url(r'^ner/$', NERView.as_view()),
    url(r'^ner-docs/$', NERWithDocIdView.as_view()),
    url(r'^versions/$', ApiVersionsView.as_view()),
    url(r'^keywords-extraction/$', KeywordsExtractionView.as_view()),
    url(r'^recommendation/$', RecommendationView.as_view()),
    url(r'^(?P<entity>[a-zA-Z\.]+)/correlation/$', CorrelationView.as_view()),
    url(r'^similarity/$', DocsSimilarityView.as_view()),
    url(r'^similardocs/$', SimilarDocsView.as_view()),
    url(r'^cluster/$', ClusteringView.as_view()),
    url(r'^cluster-data/$', ClusteringDataView.as_view()),
    url(r'^re-cluster/$', ReClusteringView.as_view()),
    url(r'^doc/$', ClassifiedDocumentView.as_view()),
    url(r'^token/$', TokenView.as_view())
]

VERSION_PATTERN = '(?P<version>[a-z0-9A-Z\.]+)'


def prepend_version_if_not(pattern):
    newpattern = pattern
    if VERSION_PATTERN not in pattern:
        newpattern = '^{}/{}'.format(
            VERSION_PATTERN,
            pattern.replace('^', '').lstrip('/')
        )
    return newpattern


# now prepend version pattern to the url patterns not having version pattern
urlpatterns += [
    url(prepend_version_if_not(x._regex), x.callback)
    for x in filter(lambda x: VERSION_PATTERN not in x._regex, urlpatterns)
]
