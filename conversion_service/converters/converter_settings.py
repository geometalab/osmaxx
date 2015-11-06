from django.conf import settings

OSMAXX_CONVERSION_SERVICE = {
    'XAPI_MIRROR': 'http://www.overpass-api.de/api/xapi_meta',
    'RESULT_DIR': '/tmp/osm/results',
    'RESULT_TTL': -1,  # never expire!
}

if hasattr(settings, 'OSMAXX_CONVERSION_SERVICE'):
    OSMAXX_CONVERSION_SERVICE.update(settings.OSMAXX_CONVERSION_SERVICE)
