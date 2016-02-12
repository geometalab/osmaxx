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


@pytest.fixture(params=format_list)
def conversion_parametrization_data(request, valid_clipping_area):
    out_format = request.param
    # TODO: parametrize the srs to test with different srses as well.
    out_srs = 4326
    clipping_area = valid_clipping_area.id
    return {'out_format': out_format, 'out_srs': out_srs, 'clipping_area': clipping_area}


@pytest.fixture(params=format_list)
def conversion_parametrization(request, valid_clipping_area):
    out_format = request.param
    # TODO: parametrize the srs to test with different srses as well.
    out_srs = 4326
    from osmaxx.conversion.models import Parametrization
    return Parametrization.objects.create(out_format=out_format, out_srs=out_srs, clipping_area=valid_clipping_area)


@pytest.fixture
def server_url():
    return 'http://backends.own.url.example.com'


@pytest.fixture
def conversion_job_data(conversion_parametrization):
    conversion_parametrization = conversion_parametrization.id
    return {'callback_url': 'http://callback.example.com', 'parametrization': conversion_parametrization}


@pytest.fixture
def conversion_job(conversion_parametrization, server_url):
    from osmaxx.conversion.models import Job
    return Job.objects.create(own_base_url=server_url, parametrization=conversion_parametrization)
