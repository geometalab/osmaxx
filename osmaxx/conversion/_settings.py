from datetime import timedelta
from django.conf import settings

CONVERSION_SETTINGS = {
    'result_harvest_interval_seconds': timedelta(minutes=1).total_seconds(),
    'PBF_PLANET_FILE_PATH': '/var/data/osm-planet/pbf/planet-latest.osm.pbf',
    'RESULT_TTL': -1,  # never expire!
}

if hasattr(settings, 'OSMAXX_CONVERSION_SERVICE'):
    CONVERSION_SETTINGS.update(settings.OSMAXX_CONVERSION_SERVICE)

# internal values, can't be overridden using Django's settings mechanism
CONVERSION_SETTINGS.update({
    'GIS_CONVERSION_DB_NAME': 'osmaxx_db',
    'GIS_CONVERSION_DB_USER': 'postgres',
    'GIS_CONVERSION_DB_PASSWORD': 'postgres',
})
