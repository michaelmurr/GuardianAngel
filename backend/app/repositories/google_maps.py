import googlemaps
from settings import env

GOOGLE_MAPS_CLIENT = googlemaps.Client(key=env.GOOGLE_MAPS_API_KEY)


def get_google_maps_client():
    return GOOGLE_MAPS_CLIENT
