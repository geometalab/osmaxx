import pytest

import osmaxx.conversion.formats
from osmaxx.conversion.converters.converter import Conversion, convert

format_list = osmaxx.conversion.formats.FORMAT_DEFINITIONS.keys()


@pytest.fixture(params=format_list)
def conversion_format(request):
    return request.param

@pytest.fixture
def area_name():
    return 'area_name'

@pytest.fixture()
def output_zip_file_path():
    return '/some/test/path/to/a/zipfile.zip'

@pytest.fixture()
def filename_prefix():
    return 'test_prefix_for_this_example'


@pytest.fixture()
def out_srs():
    return 'EPSG:4326'


def test_start_format_extraction(conversion_format, area_name, simple_osmosis_line_string, output_zip_file_path, filename_prefix, out_srs, mocker):
    gis_converter_mock_create = mocker.patch('osmaxx.conversion.converters.converter_gis.gis.GISConverter.create_gis_export')
    garmin_converter_mock_create = mocker.patch('osmaxx.conversion.converters.converter_garmin.garmin.Garmin.create_garmin_export')
    conversion = Conversion(
        conversion_format=conversion_format,
        area_name=area_name,
        osmosis_polygon_file_string=simple_osmosis_line_string,
        output_zip_file_path=output_zip_file_path,
        filename_prefix=filename_prefix,
        out_srs=out_srs,
    )
    conversion.start_format_extraction()
    assert gis_converter_mock_create.call_count + garmin_converter_mock_create.call_count == 1
