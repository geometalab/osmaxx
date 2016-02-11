import os
import pytest

import osmaxx.conversion.formats

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


@pytest.fixture
def simple_osmosis_line_string():
    return os.linesep.join([
        'none',
        '1-outer',
        '  0.000000E+00 0.000000E+00',
        '  0.000000E+00 1.000000E+00',
        '  1.000000E+00 1.000000E+00',
        '  0.000000E+00 0.000000E+00',
        'END',
        '2-outer',
        '  1.000000E+00 1.000000E+00',
        '  1.000000E+00 2.000000E+00',
        '  2.000000E+00 2.000000E+00',
        '  1.000000E+00 1.000000E+00',
        'END',
        'END',
        '',
    ])
