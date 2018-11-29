from core.models import Country
from .levenshtein import most_matching
from core.serializers import FuzzyCountrySerializer

import logging
logger = logging.getLogger('django')


def get_most_matching(query, type):
    if type == 'country':
        countries = get_most_matching_countries(query)
        return FuzzyCountrySerializer(countries, many=True).data
    return []


def get_most_matching_countries(query):
    all_countries = list(Country.objects.all())
    matching, scores = most_matching(
        query,
        all_countries,
        key=lambda x: x.name
    )
    countries_with_similarities = []

    # add similarity
    for country, similarity in zip(matching, scores):
        country.similarity = similarity
        countries_with_similarities.append(country)

    return countries_with_similarities
