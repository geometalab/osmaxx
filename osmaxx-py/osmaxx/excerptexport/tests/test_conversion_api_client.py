import os
import time
import vcr

from .copying_mock import CopyingMock
from requests.models import Response

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, ExtractionOrderState, BBoxBoundingGeometry
from osmaxx.excerptexport.services import ConversionApiClient


class ConversionApiClientTestCase(TestCase):
    def setUp(self):
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

    def _create_response(self, status_code=200, reason='OK', headers={'content-type': 'application/json'}, json={}):
        response = Response()
        response.status_code = status_code
        response.reason = reason
        response.headers = headers
        response.json = CopyingMock(return_value=json)
        return response

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

    @vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job.yml')
    def test_create_job(self):
        api_client = ConversionApiClient()
        self.assertIsNone(self.extraction_order.process_id)

        response = api_client.create_job(self.extraction_order)

        self.assertEqual(api_client.headers['Authorization'], 'JWT {token}'.format(token=api_client.token))
        self.assertIsNone(api_client.errors)
        expected_keys_in_response = ["rq_job_id", "callback_url", "status", "gis_formats", "gis_options", "extent"]
        actual_keys_in_response = list(response.json().keys())
        expected_keys_in_response.sort()
        actual_keys_in_response.sort()
        self.assertEqual(expected_keys_in_response, actual_keys_in_response)
        self.assertEqual(self.extraction_order.state, ExtractionOrderState.PROCESSING)
        self.assertEqual(self.extraction_order.process_id, response.json().get('rq_job_id'))
        self.assertIsNotNone(self.extraction_order.process_id)

    def test_download_files(self):
        cassette_file_location = 'fixtures/vcr/conversion_api-test_download_files.yml'
        cassette_empty = not os.path.exists(cassette_file_location)

        with vcr.use_cassette(cassette_file_location):
            api_client = ConversionApiClient()
            api_client.create_job(self.extraction_order)

            if cassette_empty:
                # wait for external service to complete request
                time.sleep(120)

            success = api_client.download_result_files(self.extraction_order)
            self.assertIsNone(api_client.errors)
            self.assertTrue(success)
            content_types_of_output_files = (f.content_type for f in self.extraction_order.output_files.all())
            self.assertCountEqual(content_types_of_output_files, ['fgdb', 'spatialite'])
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

    @vcr.use_cassette('fixtures/vcr/conversion_api-test_order_status_processing.yml')
    def test_order_status_processing(self):
        api_client = ConversionApiClient()

        self.assertEqual(self.extraction_order.output_files.count(), 0)
        self.assertNotEqual(self.extraction_order.state, ExtractionOrderState.PROCESSING)

        api_client.create_job(self.extraction_order)

        api_client.update_order_status(self.extraction_order)
        self.assertEqual(self.extraction_order.state, ExtractionOrderState.PROCESSING)
        self.assertEqual(self.extraction_order.output_files.count(), 0)

    def test_order_status_done(self):
        cassette_file_location = 'fixtures/vcr/conversion_api-test_order_status_done.yml'
        cassette_empty = not os.path.exists(cassette_file_location)

        with vcr.use_cassette(cassette_file_location):
            api_client = ConversionApiClient()
            api_client.create_job(self.extraction_order)
            api_client.update_order_status(self.extraction_order)  # processing
            self.assertEqual(self.extraction_order.output_files.count(), 0)
            self.assertNotEqual(self.extraction_order.state, ExtractionOrderState.FINISHED)

            if cassette_empty:
                # wait for external service to complete request
                time.sleep(120)

            api_client.update_order_status(self.extraction_order)
            self.assertEqual(self.extraction_order.state, ExtractionOrderState.FINISHED)
