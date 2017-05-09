import os
import tempfile
from collections import namedtuple

import pytest
from django.conf import settings

from osmaxx.conversion import output_format
from osmaxx.conversion.converters.converter_gis import detail_levels
from osmaxx.conversion.constants import coordinate_reference_systems as crs
from osmaxx.conversion.constants.statuses import STARTED, FAILED, FINISHED

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


@pytest.fixture(params=crs.GLOBAL_CRS[:2])
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


@pytest.fixture(params=format_list)
def conversion_parametrization_data(request, persisted_valid_clipping_area, detail_level, out_srs):
    out_format = request.param
    clipping_area = persisted_valid_clipping_area.id
    return {'out_format': out_format, 'out_srs': out_srs, 'clipping_area': clipping_area, 'detail_level': detail_level}


@pytest.fixture(params=format_list)
def conversion_parametrization(request, persisted_valid_clipping_area, detail_level, out_srs):
    out_format = request.param
    from osmaxx.conversion.models import Parametrization
    return Parametrization.objects.create(out_format=out_format, detail_level=detail_level, out_srs=out_srs, clipping_area=persisted_valid_clipping_area)


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
def conversion_job_data(conversion_parametrization):
    conversion_parametrization = conversion_parametrization.id
    return {'callback_url': 'http://callback.example.com', 'parametrization': conversion_parametrization}


@pytest.fixture
def conversion_job(conversion_parametrization, server_url):
    from osmaxx.conversion.models import Job
    return Job.objects.create(own_base_url=server_url, parametrization=conversion_parametrization)


@pytest.fixture
def started_conversion_job(conversion_parametrization, server_url, fake_rq_id):
    from osmaxx.conversion.models import Job
    return Job.objects.create(own_base_url=server_url, parametrization=conversion_parametrization, rq_job_id=fake_rq_id, status=STARTED)


@pytest.fixture
def failed_conversion_job(conversion_parametrization, server_url, fake_rq_id):
    from osmaxx.conversion.models import Job
    return Job.objects.create(own_base_url=server_url, parametrization=conversion_parametrization, rq_job_id=fake_rq_id, status=FAILED)


@pytest.fixture
def finished_conversion_job(request, conversion_parametrization, server_url, fake_rq_id, empty_zip):
    from osmaxx.conversion.models import Job
    conversion_job = Job.objects.create(own_base_url=server_url, parametrization=conversion_parametrization, rq_job_id=fake_rq_id, status=FAILED)
    conversion_job.status = FINISHED
    from osmaxx.conversion.management.commands.result_harvester import add_file_to_job
    empty_zip_path = add_file_to_job(conversion_job=conversion_job, result_zip_file=empty_zip.name)

    def remove_empty_zip_path():
        try:
            os.unlink(empty_zip_path)
        except FileNotFoundError:  # already removed by some test
            pass
    request.addfinalizer(remove_empty_zip_path)

    def remove_result_path():
        import shutil
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'job_result_files'))
    request.addfinalizer(remove_result_path)

    conversion_job.save()
    return conversion_job


@pytest.fixture
def rq_mock_return():
    def rq_enqueue_with_settings_mock_return():
        FakeRQ = namedtuple('FakeRQ', 'id')
        return FakeRQ(id=42)
    return rq_enqueue_with_settings_mock_return
