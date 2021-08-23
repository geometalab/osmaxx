import os
import environ
from datetime import timedelta
from django.conf import settings

env = environ.Env()

CONVERSION_SETTINGS = {
    "result_harvest_interval_seconds": timedelta(minutes=1).total_seconds(),
    "PBF_PLANET_FILE_PATH": "/var/data/osm-planet/pbf/planet-latest.osm.pbf",
    "SEA_AND_BOUNDS_ZIP_DIRECTORY": "/var/data/garmin/additional_data/",
    "RESULT_TTL": -1,  # never expire!
}

if hasattr(settings, "OSMAXX_CONVERSION_SERVICE"):
    CONVERSION_SETTINGS.update(settings.OSMAXX_CONVERSION_SERVICE)

# internal values, can't be overridden using Django's settings mechanism
CONVERSION_SETTINGS.update(
    {
        "GIS_CONVERSION_DB_NAME": env.str(
            "GIS_CONVERSION_DB_NAME",
            default="osmaxx_conversion_db",
        ),
        "GIS_CONVERSION_DB_USER": env.str(
            "GIS_CONVERSION_DB_USER",
            default="postgres",
        ),
        "GIS_CONVERSION_DB_PASSWORD": env.str(
            "GIS_CONVERSION_DB_PASSWORD",
            default="postgres",
        ),
        "GIS_CONVERSION_DB_HOST": env.str(
            "GIS_CONVERSION_DB_HOST",
            default=None,
        ),
        "OSM_BOUNDARIES_DB_NAME": env.str(
            "OSM_BOUNDARIES_DB_NAME",
            default="osmboundaries",
        ),
    }
)

CONVERSION_SETTINGS.update(
    {
        "CONVERSION_SCHEMA_NAME_TMP": f"{CONVERSION_SETTINGS['GIS_CONVERSION_DB_NAME']}_tmp",
        "CONVERSION_SCHEMA_NAME_TMP_VIEW": f"{CONVERSION_SETTINGS['GIS_CONVERSION_DB_NAME']}_tmp_view",
    }
)

copying_notice = os.path.join(
    os.path.dirname(__file__), "converters", "licenses", "COPYING"
)
odb_license = os.path.join(
    os.path.dirname(__file__), "converters", "licenses", "ODB_LICENSE"
)
creative_commons_license = os.path.join(
    os.path.dirname(__file__), "converters", "licenses", "CREATIVE_COMMONS_LICENSE"
)
