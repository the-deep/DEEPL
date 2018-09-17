import os
import json
from django.conf import settings

import logging
logger = logging.getLogger('django')


def get_data():
    """
    Returns array or dicts with keys: label and extra
    """
    try:
        countries_path = os.path.join(
            settings.BASE_DIR,
            'fuzzy',
            'data',
            'countries.json'
        )
        countries = json.load(open(countries_path))
    except Exception as e:
        logger.warn('Exception while loading countries.json. {}'.format(e))
    else:
        data = countries['data']
    return [
        {
            'label': x['label']['default'],
            'extra': {'iso2': x['iso2'], 'iso3': x['iso3']}
        } for x in data
    ]
