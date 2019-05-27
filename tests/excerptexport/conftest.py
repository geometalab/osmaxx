import os
import tempfile

import pytest

from osmaxx.conversion import output_format
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
    return extraction_order


def create_export(extraction_order, file_format):
    return Export.objects.create(
        extraction_order=extraction_order,
        file_format=file_format,
    )


@pytest.fixture(params=output_format.ALL)
def export(request, extraction_order):
    return create_export(
        extraction_order=extraction_order,
        file_format=request.param,
    )


@pytest.fixture
def exports(extraction_order):
    return [create_export(extraction_order, format) for format in output_format.ALL]


@pytest.fixture
def output_file(export):
    return OutputFile.objects.create(mime_type='test/plain', export=export)


@pytest.fixture
def output_file_filename():
    return 'download_file.zip'


@pytest.fixture
def output_file_content():
    return b"some content"


@pytest.yield_fixture
def some_fake_zip_file(request, output_file_content):
    tmpfile = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)

    try:
        tmpfile.write(output_file_content)
        tmpfile.seek(0)
        yield tmpfile
    finally:
        if os.path.exists(tmpfile.name):
            os.remove(tmpfile.name)


@pytest.fixture
def output_file_with_file(output_file, output_file_filename, output_file_content):
    from django.core.files.base import ContentFile
    file = ContentFile(output_file_content)
    output_file.file.save(output_file_filename, file)
    return output_file
