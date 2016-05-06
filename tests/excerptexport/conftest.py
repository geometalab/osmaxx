import pytest


@pytest.fixture
def bounding_geometry():
    from django.contrib.gis import geos
    return geos.GEOSGeometry(
        '{"type":"MultiPolygon","coordinates":[[[[8.815935552120209,47.222220486817676],[8.815935552120209,47.22402752311505],[8.818982541561127,47.22402752311505],[8.818982541561127,47.222220486817676],[8.815935552120209,47.222220486817676]]]]}'
    )
