import os

from django.conf import settings

OSMAXX_CONVERSION_SERVICE = {
    'PBF_PLANET_FILE_PATH': '/var/data/osm-planet/planet-latest.osm.pbf',
    'RESULT_DIR': '/tmp/osmaxx-conversion-service/results',
    'RESULT_TTL': -1,  # never expire!
    'ESTIMATION_CSV_SOURCE_FILE': os.path.join(os.path.dirname(__file__), '..', 'file_size_estimation', 'planet-stats.csv'),
}

if hasattr(settings, 'OSMAXX_CONVERSION_SERVICE'):
    OSMAXX_CONVERSION_SERVICE.update(settings.OSMAXX_CONVERSION_SERVICE)

# internal values, can't be overridden but are kept centralized
OSMAXX_CONVERSION_SERVICE.update({
    'GIS_CONVERSION_DB_NAME': 'osmaxx_db',
    'GIS_CONVERSION_DB_USER': 'postgres',
    'GIS_CONVERSION_DB_PASSWORD': None,
})
