import random
from contextlib import closing

import pytest
import sqlalchemy
from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.geos.collections import GeometryCollection
from sqlalchemy import select, func
from sqlalchemy.engine.url import URL as DBURL

from osmaxx.conversion_api.coordinate_reference_systems import WGS_84
from osmaxx.geodesy.coordinate_reference_system import UTMZone, wrap_longitude_degrees, utm_zones_for_representing
from tests.utils import slow


def test_coordinate_system_of_geom_does_not_matter():
    # ... except for rounding/gimbal lock effects. Due to these effects, we cannot use transformable_geom fixture here.
    geom_wgs84 = GeometryCollection(Point(5.0, 23.0), srid=WGS_84)
    geom_utm31n = geom_wgs84.transform(UTMZone('north', 31).srid, clone=True)
    assert utm_zones_for_representing(geom_wgs84) == utm_zones_for_representing(geom_utm31n)


def test_naive_zone_of_geom_amongst_zones_to_represent_the_geom(transformable_geom, utm_zone):
    assert utm_zone in utm_zones_for_representing(transformable_geom)


def test_naive_antipodal_zone_of_geom_not_amongst_zones_to_represent_the_geom(untransformable_geom, utm_zone):
    assert utm_zone not in utm_zones_for_representing(untransformable_geom)


def test_utm_zone_treats_transformable_geom_as_representable(transformable_geom, utm_zone):
    assert utm_zone.can_represent(transformable_geom)


def test_utm_zone_treats_untransformable_geom_as_unrepresentable(untransformable_geom, utm_zone):
    assert not utm_zone.can_represent(untransformable_geom)


def test_transformation_to_utm_with_geodjango_geos(transformable_geom, utm_zone):
    transformable_geom.transform(utm_zone.srid)


def test_utm_zone_str():
    assert str(UTMZone('north', 5)) == "UTM Zone 5, northern hemisphere"
    assert str(UTMZone('south', 23)) == "UTM Zone 23, southern hemisphere"


def test_utm_zone_repr():
    assert repr(UTMZone('north', 5)) == "UTMZone('north', 5)"
    assert repr(UTMZone('south', 23)) == "UTMZone('south', 23)"


@slow
def test_transformation_to_utm_with_geoalchemy2(transformable_geom, utm_zone):
    django_db_config = settings.DATABASES['default']
    db_config = dict(
        username=django_db_config['USER'],
        password=django_db_config['PASSWORD'],
        database=django_db_config['NAME'],
        host=django_db_config['HOST'],
        port=django_db_config['PORT'],
    )
    engine = sqlalchemy.create_engine(DBURL('postgres', **db_config))

    query = select([func.ST_Transform(func.ST_GeomFromText(transformable_geom.ewkt), utm_zone.srid)])
    with closing(engine.execute(query)) as result:
        assert result.rowcount == 1


@pytest.fixture(params=['collection', 'point'])
def untransformable_geom(request, untransformable_point):
    wrapper = dict(
        collection=GeometryCollection,
        point=lambda p, srid: p,
    )
    return wrapper[request.param](untransformable_point, srid=untransformable_point.srid)


@pytest.fixture(params=['collection', 'point'])
def transformable_geom(request, transformable_point):
    wrapper = dict(
        collection=GeometryCollection,
        point=lambda p, srid: p,
    )
    return wrapper[request.param](transformable_point, srid=transformable_point.srid)


@pytest.fixture
def untransformable_point(transformable_point):
    # antipodal point of a transformable point
    return Point(
        x=wrap_longitude_degrees(transformable_point.x + 180),
        y=-transformable_point.y,
        srid=WGS_84,
    )


@pytest.fixture
def transformable_point(transformable_point_longitude_degrees, transformable_point_latitude_degrees):
    return Point(transformable_point_longitude_degrees, transformable_point_latitude_degrees, srid=WGS_84)


@pytest.fixture(params=[-UTMZone.MAX_LONGITUDE_OFFSET, -23.0, 0, UTMZone.MAX_LONGITUDE_OFFSET])
def transformable_point_longitude_degrees(request, utm_zone):
    return wrap_longitude_degrees(utm_zone.central_meridian_longitude_degrees + request.param)


@pytest.fixture(params=[-90, -5, 0, 90])
def transformable_point_latitude_degrees(request):
    return request.param


@pytest.fixture
def utm_zone(hemisphere, utm_zone_number):
    return UTMZone(hemisphere=hemisphere, utm_zone_number=utm_zone_number)


@pytest.fixture(params=UTMZone.HEMISPHERE_PREFIXES.keys())
def hemisphere(request):
    return request.param

utm_zone_numbers = UTMZone.VALID_ZONE_NUMBERS
if not pytest.config.getoption("--all-utm-zones"):
    utm_zone_numbers = random.sample(utm_zone_numbers, 3)


@pytest.fixture(params=utm_zone_numbers)
def utm_zone_number(request):
    return request.param
