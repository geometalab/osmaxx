from osmaxx.conversion._settings import CONVERSION_SETTINGS
from osmaxx.conversion.converters.converter_gis.helper.postgres_wrapper import Postgres


def get_default_postgres_wrapper():
    conversion_service_settings = CONVERSION_SETTINGS
    return Postgres(
        user=conversion_service_settings["GIS_CONVERSION_DB_USER"],
        password=conversion_service_settings["GIS_CONVERSION_DB_PASSWORD"],
        db_name=conversion_service_settings["GIS_CONVERSION_DB_NAME"],
        host=conversion_service_settings["GIS_CONVERSION_DB_HOST"],
    )
