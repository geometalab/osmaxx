from osmaxx.converters.converter_settings import OSMAXX_CONVERSION_SERVICE
from osmaxx.converters.gis_converter.helper.postgres_wrapper import Postgres


def get_default_postgres_wrapper():
    conversion_service_settings = OSMAXX_CONVERSION_SERVICE
    return Postgres(
        user=conversion_service_settings['GIS_CONVERSION_DB_USER'],
        password=conversion_service_settings['GIS_CONVERSION_DB_PASSWORD'],
        db_name=conversion_service_settings['GIS_CONVERSION_DB_NAME'],
    )
