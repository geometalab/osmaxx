import pytest


@pytest.mark.django_db()
def test_osmosis_polygon_file_string_property_returns_osmosis_polygon_file(valid_clipping_area):
    assert valid_clipping_area.osmosis_polygon_file_string is not None
    assert valid_clipping_area.osmosis_polygon_file_string != ''


@pytest.mark.django_db()
def test_representation(valid_clipping_area):
    assert str(valid_clipping_area) is not None
    assert str(valid_clipping_area) == "test (1)"
