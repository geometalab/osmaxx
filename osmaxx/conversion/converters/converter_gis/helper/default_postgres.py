from osmaxx.conversion._settings import CONVERSION_SETTINGS
from osmaxx.conversion.converters.converter_gis.helper.postgres_wrapper import Postgres


def get_default_postgres_wrapper(user=None, password=None, db_name=None, host=None):
    conversion_service_settings = CONVERSION_SETTINGS
    return Postgres(
        user=user or conversion_service_settings["GIS_CONVERSION_DB_USER"],
        password=password or conversion_service_settings["GIS_CONVERSION_DB_PASSWORD"],
        db_name=db_name or conversion_service_settings["GIS_CONVERSION_DB_NAME"],
        host=host or conversion_service_settings["GIS_CONVERSION_DB_HOST"],
    )
