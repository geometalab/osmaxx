import time
from unittest import mock
from unittest.mock import Mock, sentinel
from urllib.parse import urlparse

import os
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.test.testcases import TestCase
from hamcrest import assert_that, contains_inanyorder, matches_regexp, match_equality

from osmaxx.api_client import ConversionApiClient
from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, ExtractionOrderState, BBoxBoundingGeometry
from osmaxx.job_progress.views import tracker
from tests.test_helpers import vcr_explicit_path as vcr, absolute_cassette_lib_path


class ConversionApiClientAuthTestCase(TestCase):
    @vcr.use_cassette('fixtures/vcr/conversion_api-test_successful_login.yml')
    def test_successful_login(self):
        api_client = ConversionApiClient()

        self.assertIsNone(api_client.token)

        success = api_client.login()

        self.assertTrue(success)
        self.assertIsNotNone(api_client.token)

    @vcr.use_cassette('fixtures/vcr/conversion_api-test_failed_login.yml')
    def test_failed_login(self):
        api_client = ConversionApiClient()
        api_client.password = 'invalid'

        self.assertEqual(api_client.password, 'invalid')
        self.assertIsNone(api_client.token)

        success = api_client.login()

        self.assertEqual({'non_field_errors': ['Unable to login with provided credentials.']}, api_client.errors)
        self.assertIsNone(api_client.token)
        self.assertFalse(success)


class ConversionApiClientTestCase(TestCase):
    def setUp(self):
        self.request = Mock()
        self.request.build_absolute_uri.return_value = 'http://the-host.example.com/job_progress/tracker/1/'
        self.user = User.objects.create_user('user', 'user@example.com', 'pw')
        self.bounding_box = BBoxBoundingGeometry.create_from_bounding_box_coordinates(
            40.77739734768811, 29.528980851173397, 40.77546776498174, 29.525547623634335
        )
        self.excerpt = Excerpt.objects.create(
            name='Neverland', is_active=True, is_public=True, owner=self.user, bounding_geometry=self.bounding_box
        )
        self.extraction_order = ExtractionOrder.objects.create(excerpt=self.excerpt, orderer=self.user)
        self.extraction_order.extraction_configuration = {
            'gis_formats': ['fgdb', 'spatialite'],
            'gis_options': {
                'coordinate_reference_system': 'WGS_84',
                'detail_level': 1
            }
        }
        self.api_client = ConversionApiClient()

    #
    # Unit tests:

    @mock.patch.object(ConversionApiClient, 'create_job', side_effect=[sentinel.job_1, sentinel.job_2])
    @mock.patch.object(
        ConversionApiClient, 'create_parametrization',
        create=True,  # TODO: remove 'create' once implemented
        side_effect=[sentinel.parametrization_1, sentinel.parametrization_2],
    )
    @mock.patch.object(ConversionApiClient, 'create_boundary', create=True)  # TODO: remove 'create' once implemented
    def test_extraction_order_forward_to_conversion_service(
            self, create_boundary_mock, create_parametrization_mock, create_job_mock):
        result = self.extraction_order.forward_to_conversion_service(incoming_request=self.request)

        create_boundary_mock.assert_called_once_with(self.bounding_box.geometry)
        gis_conversion_options = self.extraction_order.extraction_configuration['gis_options']
        assert_that(
            create_parametrization_mock.mock_calls, contains_inanyorder(
                mock.call(create_boundary_mock.return_value, 'fgdb', gis_conversion_options),
                mock.call(create_boundary_mock.return_value, 'spatialite', gis_conversion_options),
            )
        )
        assert_that(
            create_job_mock.mock_calls, contains_inanyorder(
                mock.call(sentinel.parametrization_1, self.request),
                mock.call(sentinel.parametrization_2, self.request),
            )
        )
        assert_that(
            result, contains_inanyorder(
                sentinel.job_1,
                sentinel.job_2,
            )
        )

    #
    # Integration tests:

    # TODO: re-record VCR (service API has changed)

    @vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job.yml')
    def test_create_job(self):
        self.api_client.login()
        self.assertIsNone(self.extraction_order.process_id)

        response = self.api_client.create_job(self.extraction_order, request=self.request)

        self.assertEqual(self.api_client.headers['Authorization'], 'JWT {token}'.format(token=self.api_client.token))
        self.assertIsNone(self.api_client.errors)
        expected_keys_in_response = ["rq_job_id", "callback_url", "status", "gis_formats", "gis_options", "extent"]
        actual_keys_in_response = list(response.json().keys())
        self.assertCountEqual(expected_keys_in_response, actual_keys_in_response)
        self.assertEqual(self.extraction_order.state, ExtractionOrderState.QUEUED)
        self.assertEqual(self.extraction_order.process_id, response.json().get('rq_job_id'))
        self.assertIsNotNone(self.extraction_order.process_id)
        self.request.build_absolute_uri.assert_called_with(match_equality(matches_regexp('/job_progress/tracker/\d+/')))

    @vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job.yml')  # Intentionally same as for test_create_job()
    def test_callback_url_of_created_job_resolves_to_job_updater(self):
        self.api_client.login()
        self.assertIsNone(self.extraction_order.process_id)

        response = self.api_client.create_job(self.extraction_order, request=self.request)

        callback_url = response.json()['callback_url']
        scheme, host, callback_path, params, *_ = urlparse(callback_url)

        match = resolve(callback_path)
        self.assertEqual(match.func, tracker)
        self.request.build_absolute_uri.assert_called_with(match_equality(matches_regexp('/job_progress/tracker/\d+/')))

    @vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job.yml')  # Intentionally same as for test_create_job()
    def test_callback_url_of_created_job_refers_to_correct_extraction_order(self):
        self.api_client.login()
        self.assertIsNone(self.extraction_order.process_id)

        response = self.api_client.create_job(self.extraction_order, request=self.request)

        callback_url = response.json()['callback_url']
        scheme, host, callback_path, params, *_ = urlparse(callback_url)

        match = resolve(callback_path)
        self.assertEqual(match.kwargs, {'order_id': str(self.extraction_order.id)})
        self.request.build_absolute_uri.assert_called_with(match_equality(matches_regexp('/job_progress/tracker/\d+/')))

    @vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job.yml')  # Intentionally same as for test_create_job()
    def test_callback_url_would_reach_this_django_instance(self):
        self.api_client.login()
        self.assertIsNone(self.extraction_order.process_id)

        response = self.api_client.create_job(self.extraction_order, request=self.request)

        callback_url = response.json()['callback_url']
        scheme, host, callback_path, params, *_ = urlparse(callback_url)
        assert scheme.startswith('http')  # also matches https
        self.assertEqual(host, 'the-host.example.com')
        self.request.build_absolute_uri.assert_called_with(match_equality(matches_regexp('/job_progress/tracker/\d+/')))

    def test_download_files(self):
        cassette_file_location = os.path.join(
            absolute_cassette_lib_path,
            'fixtures/vcr/conversion_api-test_download_files.yml'
        )
        cassette_empty = not os.path.exists(cassette_file_location)

        with vcr.use_cassette(cassette_file_location):
            self.api_client.login()
            self.api_client.create_job(self.extraction_order, request=self.request)

            if cassette_empty:
                # wait for external service to complete request
                time.sleep(120)

            self.api_client._download_result_files(
                self.extraction_order,
                job_status=self.api_client.job_status(self.extraction_order)
            )
            self.assertIsNone(self.api_client.errors)
            content_types_of_output_files = (f.content_type for f in self.extraction_order.output_files.all())
            ordered_formats = self.extraction_order.extraction_configuration['gis_formats']
            self.assertCountEqual(content_types_of_output_files, ordered_formats)
            self.assertAlmostEqual(
                len(self.extraction_order.output_files.order_by('id')[0].file.read()),
                446005,
                delta=10000
            )
            self.assertAlmostEqual(
                len(self.extraction_order.output_files.order_by('id')[1].file.read()),
                368378,
                delta=10000
            )
        self.request.build_absolute_uri.assert_called_with(match_equality(matches_regexp('/job_progress/tracker/\d+/')))

    def test_order_status_processing(self):
        cassette_file_location = os.path.join(
            absolute_cassette_lib_path,
            'fixtures/vcr/conversion_api-test_order_status_processing.yml'
        )
        cassette_empty = not os.path.exists(cassette_file_location)
        with vcr.use_cassette(cassette_file_location):
            self.api_client.login()

            self.assertEqual(self.extraction_order.output_files.count(), 0)
            self.assertNotEqual(self.extraction_order.state, ExtractionOrderState.PROCESSING)
            self.assertEqual(self.extraction_order.state, ExtractionOrderState.INITIALIZED)

            self.api_client.create_job(self.extraction_order, request=self.request)

            if cassette_empty:
                time.sleep(10)

            self.api_client.update_order_status(self.extraction_order)
            self.assertEqual(self.extraction_order.state, ExtractionOrderState.PROCESSING)
            self.assertNotEqual(self.extraction_order.state, ExtractionOrderState.INITIALIZED)
            self.assertEqual(self.extraction_order.output_files.count(), 0)
        self.request.build_absolute_uri.assert_called_with(match_equality(matches_regexp('/job_progress/tracker/\d+/')))

    def test_order_status_done(self):
        cassette_file_location = os.path.join(
            absolute_cassette_lib_path,
            'fixtures/vcr/conversion_api-test_order_status_done.yml'
        )
        cassette_empty = not os.path.exists(cassette_file_location)

        with vcr.use_cassette(cassette_file_location):
            self.api_client.login()
            self.api_client.create_job(self.extraction_order, request=self.request)
            self.api_client.update_order_status(self.extraction_order)  # processing
            self.assertEqual(self.extraction_order.output_files.count(), 0)
            self.assertNotEqual(self.extraction_order.state, ExtractionOrderState.FINISHED)

            if cassette_empty:
                # wait for external service to complete request
                time.sleep(120)

            self.api_client.update_order_status(self.extraction_order)
            self.assertEqual(self.extraction_order.state, ExtractionOrderState.FINISHED)
        self.request.build_absolute_uri.assert_called_with(match_equality(matches_regexp('/job_progress/tracker/\d+/')))
