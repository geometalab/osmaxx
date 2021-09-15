from osmaxx.conversion.conversion_settings import CONVERSION_SETTINGS
from osmaxx.conversion.converters.converter_gis.helper.postgres_wrapper import Postgres


def get_default_postgres_wrapper(
    db_name, user=None, password=None, host=None, search_path=None
):
    assert db_name is not None
    conversion_service_settings = CONVERSION_SETTINGS
    return Postgres(
        db_name=db_name,
        user=user or conversion_service_settings["GIS_CONVERSION_DB_USER"],
        password=password or conversion_service_settings["GIS_CONVERSION_DB_PASSWORD"],
        host=host or conversion_service_settings["GIS_CONVERSION_DB_HOST"],
        search_path=search_path,
    )
