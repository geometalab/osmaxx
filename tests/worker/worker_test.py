# pylint: disable=C0111
from urllib.parse import urlparse, urlunparse, parse_qs

import requests
from collections import namedtuple
from unittest.mock import patch, Mock, ANY, call as mock_call

from django.test import TestCase
from django_rq import get_connection
from rest_framework.reverse import reverse
from rq.job import Job

from converters.boundaries import BBox
from converters.converter import Conversion
from converters import Options
from converters import garmin_converter
from job_dispatcher.rq_helper import rq_enqueue_with_settings
from shared import ConversionProgress
from worker import converter_job
from tests.redis_test_helpers import perform_all_jobs_sync
from worker.converter_job import Notifier


class WorkerTest(TestCase):
    pbf_file_path = '/some_path/to/pbf.pbf'

    @patch('os.remove')
    @patch.object(Conversion, '_copy_statistics_file_to_format_dir', return_value=None)
    @patch.object(Conversion, '_create_statistics', return_value=None)
    @patch.object(Conversion, '_export_from_db_to_format', return_value=None)
    @patch('converters.gis_converter.bootstrap.bootstrap.boostrap', return_value=None)
    @patch('converters.osm_cutter.cut_osm_extent', return_value=pbf_file_path)
    def test_convert_calls_cut_osm_extent_and_bootstrap(  # pylint: disable=W0613
            self,
            cut_osm_extent_mock, bootstrap_mock, _export_from_db_to_format_mock,
            *args, **kwargs
    ):
        geometry = BBox(29.525547623634335, 40.77546776498174, 29.528980851173397, 40.77739734768811)
        format_options = Options(output_formats=['fgdb', 'spatialite', 'shp', 'gpkg'])
        converter_job.convert(
            geometry=geometry, format_options=format_options, callback_url=None, output_directory='/tmp/',
            protocol='http'
        )
        cut_osm_extent_mock.assert_called_once_with(geometry)
        bootstrap_mock.assert_called_once_with(self.pbf_file_path)
        self.assert_mock_has_exactly_calls(
            _export_from_db_to_format_mock,
            [mock_call(ANY, f) for f in format_options.get_output_formats()],
            any_order=True,
        )

    def assert_mock_has_exactly_calls(self, mocked_function, calls, any_order=False):
        assert_calls_equal = self.assertCountEqual if any_order else self.assertEqual
        assert_calls_equal(mocked_function.mock_calls, list(calls))

    def test_set_progress_on_job_sets_the_progress(self):
        job = rq_enqueue_with_settings(converter_job.set_progress_on_job, ConversionProgress.SUCCESSFUL)
        perform_all_jobs_sync()
        job_fetched = Job.fetch(job.id, connection=get_connection())
        self.assertDictEqual(job_fetched.meta, {'progress': ConversionProgress.SUCCESSFUL})


class ConversionTest(TestCase):
    pbf_file_path = '/some_path/to/pbf.pbf'
    mocked_job_id = '0' * 36
    rq_job_stub = namedtuple('RQJob', ['id', 'meta', 'save'])(
        id=mocked_job_id,
        meta={'progress': ''},
        save=Mock(),
    )

    @patch('os.remove')
    @patch.object(Conversion, '_copy_statistics_file_to_format_dir', return_value=None)
    @patch.object(Conversion, '_create_statistics', return_value=None)
    @patch.object(Conversion, '_export_from_db_to_format', return_value=None)
    @patch('converters.gis_converter.bootstrap.bootstrap.boostrap', return_value=None)
    @patch('converters.osm_cutter.cut_osm_extent', return_value=pbf_file_path)
    @patch('rq.get_current_job', return_value=rq_job_stub)
    @patch('worker.converter_job.Notifier')
    def test_convert_with_host_and_job_assembles_url_correctly(self, notifier_mock, rq_job_stub, *args, **kwargs):
        format_options = Options(output_formats=['fgdb', 'spatialite', 'shp', 'gpkg'])
        geometry, output_directory, callback_url = None, '/tmp/', None
        host = 'converter-host.example.com'
        protocol = 'http'
        converter_job.convert(geometry, format_options, output_directory, callback_url, protocol, host)
        expected_url = protocol + '://' + host + reverse(viewname='conversion_job_result-detail', kwargs={'rq_job_id': self.mocked_job_id})
        notifier_mock.assert_called_with(callback_url, expected_url)

    @patch('os.remove')
    @patch('converters.osm_cutter.cut_osm_extent', return_value=pbf_file_path)
    @patch.object(Conversion, '_create_garmin_export', return_value=None)
    def test_convert_with_garmin_gets_called_correctly(
            self, create_garmin_export_mock, *args, **kwargs):
        output_directory = '/tmp/'
        garmin_options = garmin_converter.options
        conversion = Conversion(garmin_options.get_output_formats(), output_directory, self.pbf_file_path)
        conversion.start_format_extraction()
        create_garmin_export_mock.assert_called_with(garmin_options.get_output_formats())


class NotifierTest(TestCase):
    @patch.object(requests.sessions.Session, 'send')
    def test_notify_calls_url_with_status_parameter(self, requests_send_mock):
        notifier = Notifier(
            callback_url='http://osmaxx-ui.example.com/update_job_status/',
            status_url='https://osmaxx-conversion.example.com/example_job/status'
        )
        notifier.notify()
        requests_send_args, requests_send_kwargs = requests_send_mock.call_args
        request = self._get_request(*requests_send_args, **requests_send_kwargs)
        url_components = urlparse(request.url)
        self.assertEqual(urlunparse(url_components._replace(query='')), notifier.callback_url)
        self.assertEqual(parse_qs(url_components.query), dict(status=[notifier.status_url]))

    @patch.object(requests.sessions.Session, 'send')
    def test_notify_without_callback_url_sends_no_request(self, requests_send_mock):
        notifier = Notifier(
            callback_url=None,
            status_url='https://osmaxx-conversion.example.com/example_job/status'
        )
        notifier.notify()
        self.assertEqual(requests_send_mock.call_count, 0)

    @patch.object(requests.sessions.Session, 'send')
    def test_notify_without_status_url_raises_value_error(self, requests_send_mock):
        notifier = Notifier(
            callback_url='http://osmaxx-ui.example.com/update_job_status/',
            status_url=None
        )
        self.assertRaises(
            ValueError,
            notifier.notify
        )

    def _get_request(self, request, **kwargs):
        return request
