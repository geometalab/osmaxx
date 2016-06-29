from contextlib import closing

import pytest
import sqlalchemy
from django.conf import settings
from django.contrib.gis.geos import Point
from sqlalchemy.engine.url import URL as DBURL
from sqlalchemy import select, func

from osmaxx.conversion_api.coordinate_reference_systems import WGS_84
from tests.inside_worker_test.conftest import slow

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


class UniversalTransverseMercatorZone:
    HEMISPHERE_PREFIXES = dict(
        north=326,
        south=327,
    )
    NUMBER_OF_ZONES_PER_HEMISPHERE = 60
    ZONE_WIDTH_DEGREES = 360 / NUMBER_OF_ZONES_PER_HEMISPHERE

    def __init__(self, hemisphere, utm_zone_number):
        assert hemisphere in self.HEMISPHERE_PREFIXES.keys()
        assert utm_zone_number - 1 in range(60)
        self.hemisphere = hemisphere
        self.utm_zone_number = utm_zone_number

    @property
    def srid(self):
        return self.HEMISPHERE_PREFIXES[self.hemisphere] * 100 + self.utm_zone_number

    @property
    def central_meridian_longitude_degrees(self):
        return -180 + (self.utm_zone_number - 0.5) * self.ZONE_WIDTH_DEGREES


@pytest.fixture(params=UniversalTransverseMercatorZone.HEMISPHERE_PREFIXES.keys())
def hemisphere(request):
    return request.param


@pytest.fixture(params=range(1, 60 + 1))
def utm_zone_number(request):
    return request.param
