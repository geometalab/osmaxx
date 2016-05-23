import pytest

from osmaxx.conversion_api import formats
from osmaxx.excerptexport.models import Export, ExtractionOrder, Excerpt


@pytest.fixture
def bounding_geometry():
    from django.contrib.gis import geos
    return geos.GEOSGeometry(
        '{"type":"MultiPolygon","coordinates":[[[[8.815935552120209,47.222220486817676],[8.815935552120209,47.22402752311505],[8.818982541561127,47.22402752311505],[8.818982541561127,47.222220486817676],[8.815935552120209,47.222220486817676]]]]}'
    )


@pytest.fixture
def excerpt(user, bounding_geometry, db):
    return Excerpt.objects.create(
        name='Neverland', is_active=True, is_public=True, owner=user, bounding_geometry=bounding_geometry
    )


@pytest.fixture
def extraction_order(excerpt, user, db):
    extraction_order = ExtractionOrder.objects.create(excerpt=excerpt, orderer=user)
    extraction_order.extraction_configuration = {}
    return extraction_order


@pytest.fixture(
    params=[formats.FGDB, formats.SHAPEFILE, formats.GPKG, formats.SPATIALITE, formats.GARMIN]
)
def export(request, extraction_order):
    return Export.objects.create(
        extraction_order=extraction_order,
        file_format=request.param
    )
