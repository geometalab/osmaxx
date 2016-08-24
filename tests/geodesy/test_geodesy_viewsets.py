import pytest
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import Polygon
from rest_framework import status
from rest_framework.reverse import reverse

from osmaxx.conversion_api.coordinate_reference_systems import WGS_84


@pytest.fixture
def polygon_1():
    return Polygon(((0, 0), (0, 1), (1, 1), (0, 0)), srid=WGS_84)


@pytest.fixture
def polygon_2():
    return Polygon(((1, 1), (1, 2), (2, 2), (1, 1)), srid=WGS_84)


@pytest.fixture
def multi_polygon():
    return MultiPolygon(polygon_1(), polygon_2(), srid=WGS_84)


@pytest.fixture(params=[polygon_1, polygon_2, multi_polygon])
def geometry(request):
    return request.param()


def test_utm_zones_returns_utm_zones(geometry, authenticated_api_client):
    utm_zone_url = reverse('geodesy_api:utm_zones-list')
    response = authenticated_api_client.post(utm_zone_url, {'geometry': geometry})
    assert response.status_code == status.HTTP_201_CREATED
    assert 'utm_zones' in response.json()


def test_utm_zones_returns_access_denied_if_not_authenticated(api_client, geometry):
    utm_zone_url = reverse('geodesy_api:utm_zones-list')
    response = api_client.post(utm_zone_url, {'geometry': geometry})
    assert response.status_code == status.HTTP_403_FORBIDDEN
