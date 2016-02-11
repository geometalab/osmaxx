import pytest

import osmaxx.conversion.formats
from osmaxx.conversion.converters.converter import Conversion
from osmaxx.conversion.converters.converter_garmin.garmin import Garmin
from osmaxx.conversion.converters.converter_gis.gis import GISConverter

format_list = osmaxx.conversion.formats.FORMAT_DEFINITIONS.keys()


@pytest.fixture(params=format_list)
def conversion_format(request):
    return request.param


def test_start_format_extraction(conversion_format, simple_osmosis_line_string, mocker):
    mocker.patch('osmaxx.conversion.converters.converter_gis.gis.GISConverter.create_gis_export')
    mocker.patch('osmaxx.conversion.converters.converter_garmin.garmin.Garmin.create_garmin_export')
    conversion = Conversion(
        conversion_format=conversion_format,
        area_name='test_area',
        osmosis_polygon_file_string=simple_osmosis_line_string,
        output_zip_file_path='/some/test/path/to/a/zipfile.zip',
        filename_prefix='test_prefix_for_this_example'
    )
    conversion.start_format_extraction()
    assert Garmin.create_garmin_export.call_count + GISConverter.create_gis_export.call_count == 1
