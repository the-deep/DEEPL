from django.conf import settings
import requests
import json


GOOGLE_GEOCODE_URL =\
    'https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}'


def get_google_geocode_url(location):
    return GOOGLE_GEOCODE_URL.format(
        getattr(settings, 'GOOGLE_API_KEY', ''),
        location,
    )


def get_location_info(location):
    r = requests.get(get_google_geocode_url(location))
    try:
        info = json.loads(r.text)
        print(info)
        return info.get('results')[0]
    except (ValueError, IndexError):
        return {}
