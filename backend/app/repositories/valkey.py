import valkey
from settings import env

VALKEY = valkey.from_url(env.REDDIS_URL)


def get_valkey():
    return VALKEY
