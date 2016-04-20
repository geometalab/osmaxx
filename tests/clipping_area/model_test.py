import pytest


@pytest.mark.django_db()
def test_osmosis_polygon_file_string_property_returns_osmosis_polygon_file(persisted_valid_clipping_area):
    # this actually assures we are testing the asserts in persisted_valid_clipping_area, if
    # at some point that fixture should be unused at other places
    pass
