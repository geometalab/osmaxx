import random
from contextlib import closing

import pytest
import sqlalchemy
from django.conf import settings
from django.contrib.gis.geos import Point
from sqlalchemy import select, func
from sqlalchemy.engine.url import URL as DBURL

from osmaxx.conversion_api.coordinate_reference_systems import WGS_84
from osmaxx.geodesy.coordinate_reference_system import UniversalTransverseMercatorZone
from tests.utils import slow

MAX_LONGITUDE_OFFSET = 90.0 - 9.9e-14


def test_transformation_to_utm_with_geodjango_geos(transformable_point, utm_zone):
    transformable_point.transform(utm_zone.srid)


@slow
def test_transformation_to_utm_with_geoalchemy2(transformable_point, utm_zone):
    django_db_config = settings.DATABASES['default']
    db_config = dict(
        username=django_db_config['USER'],
        password=django_db_config['PASSWORD'],
        database=django_db_config['NAME'],
        host=django_db_config['HOST'],
        port=django_db_config['PORT'],
    )
    engine = sqlalchemy.create_engine(DBURL('postgres', **db_config))

    query = select([func.ST_Transform(func.ST_GeomFromText(transformable_point.ewkt), utm_zone.srid)])
    with closing(engine.execute(query)) as result:
        assert result.rowcount == 1


@pytest.fixture
def transformable_point(transformable_point_longitude_degrees, transformable_point_latitude_degrees):
    return Point(transformable_point_longitude_degrees, transformable_point_latitude_degrees, srid=WGS_84)


@pytest.fixture(params=[-MAX_LONGITUDE_OFFSET, -23.0, 0, MAX_LONGITUDE_OFFSET])
def transformable_point_longitude_degrees(request, utm_zone):
    return utm_zone.central_meridian_longitude_degrees + request.param


@pytest.fixture(params=[-90, -5, 0, 90])
def transformable_point_latitude_degrees(request):
    return request.param


@pytest.fixture
def utm_zone(hemisphere, utm_zone_number):
    return UniversalTransverseMercatorZone(hemisphere=hemisphere, utm_zone_number=utm_zone_number)


@pytest.fixture(params=UniversalTransverseMercatorZone.HEMISPHERE_PREFIXES.keys())
def hemisphere(request):
    return request.param

utm_zone_numbers = range(1, 60 + 1)
if not pytest.config.getoption("--all-utm-zones"):
    utm_zone_numbers = random.sample(utm_zone_numbers, 3)


@pytest.fixture(params=utm_zone_numbers)
def utm_zone_number(request):
    return request.param
