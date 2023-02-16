import os
import tempfile
from collections import namedtuple

import pytest
from django.conf import settings

from osmaxx.conversion import coordinate_reference_system as crs, output_format, status
from osmaxx.conversion.converters.converter_gis import detail_levels

format_list = output_format.DEFINITIONS.keys()


@pytest.fixture(params=format_list)
def conversion_format(request):
    return request.param


@pytest.fixture
def area_name():
    return 'Middle Earth'


@pytest.fixture()
def output_zip_file_path():
    return '/some/test/path/to/a/zipfile.zip'


@pytest.fixture()
def filename_prefix():
    return 'test_prefix_for_this_example'


@pytest.fixture(params=detail_levels.DETAIL_LEVEL_CHOICES)
def detail_level(request):
    return request.param[0]


@pytest.fixture(params=crs.CHOICES[:2])
def out_srs(request):
    return int(request.param[0])


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


@pytest.fixture
def server_url():
    return 'http://backends.own.url.example.com'


@pytest.fixture
def fake_rq_id():
    return 42


@pytest.fixture
def empty_zip(request):
    zip_file = tempfile.NamedTemporaryFile(suffix='.zip')

    def remove_tmp_file():
        try:
            zip_file.close()
        except FileNotFoundError:  # already removed by some test
            pass
    request.addfinalizer(remove_tmp_file)
    return zip_file


@pytest.fixture
def rq_mock_return():
    def rq_enqueue_with_settings_mock_return():
        FakeRQ = namedtuple('FakeRQ', 'id')
        return FakeRQ(id=42)
    return rq_enqueue_with_settings_mock_return
