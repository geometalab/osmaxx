import pytest

from osmaxx.conversion_api import formats
from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, Export, OutputFile


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


@pytest.fixture(params=[formats.FGDB, formats.SHAPEFILE, formats.GPKG, formats.SPATIALITE, formats.GARMIN])
def export(request, extraction_order):
    return Export.objects.create(
        extraction_order=extraction_order,
        file_format=request.param,
    )


@pytest.fixture
def output_file(export):
    return OutputFile.objects.create(mime_type='test/plain', export=export, content_type='text', file_extension='zip')


@pytest.fixture
def output_file_filename():
    return 'download_file.zip'


@pytest.fixture
def output_file_content():
    return b"some content"


@pytest.fixture
def output_file_with_file(output_file, output_file_filename, output_file_content):
    from django.core.files.base import ContentFile
    file = ContentFile(output_file_content)
    output_file.file.save(output_file_filename, file)
    return output_file
