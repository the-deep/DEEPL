from django.conf import settings
import requests
import json


from NER.models import GoogleLocationCache


GOOGLE_GEOCODE_URL =\
    'https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}'


def get_google_geocode_url(location):
    return GOOGLE_GEOCODE_URL.format(
        getattr(settings, 'GOOGLE_API_KEY', ''),
        location,
    )


def get_location_info(location):
    # First query the database, if not found, make a call
    try:
        cache = GoogleLocationCache.objects.get(_location=location.lower())
        info = cache.location_info
        # add cached
        info.update({'cached': True})
        return info
    except GoogleLocationCache.DoesNotExist:
        pass
    r = requests.get(get_google_geocode_url(location))
    try:
        info = json.loads(r.text)
        location_info = info.get('results')[0]
        # save to database
        GoogleLocationCache.objects.create(
            location=location,
            location_info=location_info
        )
        return location_info
    except (ValueError, IndexError):
        return {}
