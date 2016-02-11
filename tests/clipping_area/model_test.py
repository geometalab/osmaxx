import pytest
from django.contrib.gis.geos import Polygon, MultiPolygon

from osmaxx.clipping_area.models import ClippingArea


@pytest.fixture
def valid_clipping_area():
    poly_1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
    poly_2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
    multi_polygon = MultiPolygon(poly_1, poly_2)
    return ClippingArea.objects.create(name='test', clipping_multi_polygon=multi_polygon)


@pytest.mark.django_db()
def test_osmosis_polygon_file_string_property_returns_osmosis_polygon_file(valid_clipping_area):
    assert valid_clipping_area.osmosis_polygon_file_string is not None
    assert valid_clipping_area.osmosis_polygon_file_string != ''


@pytest.mark.django_db()
def test_representation(valid_clipping_area):
    assert str(valid_clipping_area) is not None
    assert str(valid_clipping_area) == "test (1)"
