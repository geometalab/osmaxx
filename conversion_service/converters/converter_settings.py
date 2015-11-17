from django.conf import settings

OSMAXX_CONVERSION_SERVICE = {
    'PBF_PLANET_FILE_PATH': '/var/data/osm-planet/planet-latest.osm.pbf',
    'RESULT_DIR': '/tmp/osmaxx-conversion-service/results',
    'RESULT_TTL': -1,  # never expire!
}

if hasattr(settings, 'OSMAXX_CONVERSION_SERVICE'):
    OSMAXX_CONVERSION_SERVICE.update(settings.OSMAXX_CONVERSION_SERVICE)
