import os
import shutil
from io import BytesIO
from unittest.mock import patch, ANY, call
import requests_mock
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.test.testcases import TestCase

from osmaxx.excerptexport.models.bounding_geometry import BBoxBoundingGeometry
from osmaxx.excerptexport.models.excerpt import Excerpt
from osmaxx.excerptexport.models.extraction_order import ExtractionOrder, ExtractionOrderState
from osmaxx.excerptexport.models.output_file import OutputFile
from osmaxx.excerptexport.services.conversion_api_client import ConversionApiClient
from osmaxx.job_progress import views
from rest_framework.test import APITestCase, APIRequestFactory


class CallbackHandlingTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'pw')
        self.bounding_box = BBoxBoundingGeometry.create_from_bounding_box_coordinates(
            40.77739734768811, 29.528980851173397, 40.77546776498174, 29.525547623634335
        )
        self.excerpt = Excerpt.objects.create(
            name='Neverland', is_active=True, is_public=True, owner=self.user, bounding_geometry=self.bounding_box
        )
        self.extraction_order = ExtractionOrder.objects.create(
            excerpt=self.excerpt,
            orderer=self.user,
            process_id='53880847-faa9-43eb-ae84-dd92f3803a28',
        )
        self.extraction_order.extraction_configuration = {
            'gis_formats': ['fgdb', 'spatialite'],
            'gis_options': {
                'coordinate_reference_system': 'WGS_84',
                'detail_level': 1
            }
        }
        self.nonexistant_extraction_order_id = 999
        self.assertRaises(
            ExtractionOrder.DoesNotExist,
            ExtractionOrder.objects.get, pk=self.nonexistant_extraction_order_id
        )
        self.fgdb_started_and_spatialite_queued_response = {
            "rq_job_id": "53880847-faa9-43eb-ae84-dd92f3803a28",
            "status": "started",
            "progress": "started",
            "gis_formats": [
                {
                    "format": "fgdb",
                    "progress": "started",
                    "result_url": None
                },
                {
                    "format": "spatialite",
                    "progress": "queued",
                    "result_url": None
                }
            ]
        }
        self.fgdb_and_spatialite_successful_response = {
            "rq_job_id": "53880847-faa9-43eb-ae84-dd92f3803a28",
            "status": "done",
            "progress": "successful",
            "gis_formats": [
                {
                    "format": "fgdb",
                    "progress": "successful",
                    "result_url": "http://localhost:8901/api/gis_format/27/download_result/"
                },
                {
                    "format": "spatialite",
                    "progress": "successful",
                    "result_url": "http://localhost:8901/api/gis_format/28/download_result/"
                }
            ]
        }

    def test_calling_tracker_with_nonexistant_extraction_order_raises_404_not_found(self):
        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(order_id=self.nonexistant_extraction_order_id)),
            data=dict(status='http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/')
        )

        self.assertRaises(
            Http404,
            views.tracker, request, order_id=str(self.nonexistant_extraction_order_id)
        )
        request.resolver_match

    @patch('osmaxx.excerptexport.services.conversion_api_client.ConversionApiClient.login', return_value=True)
    @patch.object(ConversionApiClient, 'authorized_get', ConversionApiClient.get)  # circumvent authorization logic
    @requests_mock.Mocker(kw='requests')
    def test_calling_tracker_when_status_query_indicates_started_updates_extraction_order_state(self, *args, **mocks):
        requests_mock = mocks['requests']
        requests_mock.get(
            'http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/',
            json=self.fgdb_started_and_spatialite_queued_response
        )

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(order_id=self.extraction_order.id)),
            data=dict(status='http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/')
        )

        views.tracker(request, order_id=str(self.extraction_order.id))
        self.extraction_order.refresh_from_db()
        self.assertEqual(self.extraction_order.state, ExtractionOrderState.PROCESSING)

    @patch('osmaxx.excerptexport.services.conversion_api_client.ConversionApiClient.login', return_value=True)
    @patch.object(ConversionApiClient, 'authorized_get', ConversionApiClient.get)  # circumvent authorization logic
    @requests_mock.Mocker(kw='requests')
    @patch('osmaxx.job_progress.views.Emissary')
    def test_calling_tracker_when_status_query_indicates_started_informs_user(
            self, emissary_class_mock, *args, **mocks):
        emissary_mock = emissary_class_mock()
        requests_mock = mocks['requests']
        requests_mock.get(
            'http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/',
            json=self.fgdb_started_and_spatialite_queued_response
        )

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(order_id=self.extraction_order.id)),
            data=dict(status='http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/')
        )

        views.tracker(request, order_id=str(self.extraction_order.id))
        emissary_mock.info.assert_called_with(
            'Extraction order #{order_id} "Neverland" is now PROCESSING.'.format(
                order_id=self.extraction_order.id
            )
        )

    @patch('osmaxx.excerptexport.services.conversion_api_client.ConversionApiClient.login', return_value=True)
    @patch.object(ConversionApiClient, 'authorized_get', ConversionApiClient.get)  # circumvent authorization logic
    @requests_mock.Mocker(kw='requests')
    @patch.object(OutputFile, 'get_absolute_url', side_effect=['/a/download', '/another/download'])
    @patch('osmaxx.job_progress.views.Emissary')
    def test_calling_tracker_when_status_query_indicates_downloads_ready_advertises_downloads(
            self, emissary_class_mock, *args, **mocks):
        emissary_mock = emissary_class_mock()
        requests_mock = mocks['requests']
        requests_mock.get(
            'http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/',
            json=self.fgdb_and_spatialite_successful_response
        )
        for available_download in self.fgdb_and_spatialite_successful_response["gis_formats"]:
            requests_mock.get(
                available_download['result_url'],
                body=BytesIO(
                    bytes("dummy {} file".format(available_download['format']), encoding='utf-8')
                )
            )

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(order_id=self.extraction_order.id)),
            data=dict(status='http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/')
        )

        views.tracker(request, order_id=str(self.extraction_order.id))
        emissary_mock.success.assert_called_with(
            'The extraction of the order #{order_id} "Neverland" has been finished.'.format(
                order_id=self.extraction_order.id,
            ),
        )
        expected_body = '\n'.join(
            [
                'The extraction order #{order_id} "Neverland" has been finished and is ready for retrieval.',
                '',
                'ESRI File Geodatabase (FileGDB): http://testserver/a/download',
                'SQLite based SpatiaLite (spatialite): http://testserver/another/download',
                '',
                'View the complete order at http://testserver/orders/{order_id}',
            ]
        )
        expected_body = expected_body.format(order_id=self.extraction_order.id)
        emissary_mock.inform_mail.assert_called_with(
            subject='Extraction Order #{order_id} "Neverland" finished'.format(
                order_id=self.extraction_order.id,
            ),
            mail_body=expected_body,
        )

    @patch('osmaxx.excerptexport.services.conversion_api_client.ConversionApiClient.login', return_value=True)
    @patch.object(ConversionApiClient, 'authorized_get', ConversionApiClient.get)  # circumvent authorization logic
    @patch('osmaxx.excerptexport.services.conversion_api_client.ConversionApiClient._download_file')  # mock download
    @requests_mock.Mocker(kw='requests')
    @patch('osmaxx.job_progress.views.Emissary')
    def test_calling_tracker_when_status_query_indicates_finished_informs_user(
            self, emissary_class_mock, *args, **mocks
    ):
        emissary_mock = emissary_class_mock()
        requests_mock = mocks['requests']
        requests_mock.get(
            'http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/',
            json={
                "rq_job_id": "53880847-faa9-43eb-ae84-dd92f3803a28",
                "status": "done",
                "progress": "successful",
                "gis_formats": [
                    {
                        "format": "fgdb",
                        "progress": "successful",
                        "result_url": "http://status.example.com"
                    },
                    {
                        "format": "spatialite",
                        "progress": "successful",
                        "result_url": "http://status.example.com"
                    }
                ]
            }
        )

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(order_id=self.extraction_order.id)),
            data=dict(status='http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/')
        )

        views.tracker(request, order_id=str(self.extraction_order.id))
        self.extraction_order.refresh_from_db()
        self.assertEqual(self.extraction_order.state, ExtractionOrderState.FINISHED)
        emissary_mock.success.assert_called_with('The extraction of the order #1 "Neverland" has been finished.')
        emissary_mock.warn.assert_not_called()
        emissary_mock.error.assert_not_called()

    @patch('osmaxx.excerptexport.services.conversion_api_client.ConversionApiClient.login', return_value=True)
    @patch.object(ConversionApiClient, 'authorized_get', ConversionApiClient.get)  # circumvent authorization logic
    @requests_mock.Mocker(kw='requests')
    @patch('osmaxx.job_progress.views.Emissary')
    def test_calling_tracker_when_status_query_indicates_error_informs_user(
            self, emissary_class_mock, *args, **mocks
    ):
        emissary_mock = emissary_class_mock()
        requests_mock = mocks['requests']
        requests_mock.get(
            'http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/',
            json={
                "rq_job_id": "53880847-faa9-43eb-ae84-dd92f3803a28",
                "status": "error",
                "progress": "error",
                "gis_formats": [
                    {
                        "format": "fgdb",
                        "progress": "error",
                        "result_url": None
                    },
                    {
                        "format": "spatialite",
                        "progress": "error",
                        "result_url": None
                    }
                ]
            }
        )

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(order_id=self.extraction_order.id)),
            data=dict(status='http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/')
        )

        views.tracker(request, order_id=str(self.extraction_order.id))
        self.extraction_order.refresh_from_db()
        self.assertEqual(self.extraction_order.state, ExtractionOrderState.FAILED)
        emissary_mock.info.assert_not_called()
        emissary_mock.warn.assert_not_called()
        emissary_mock.error.assert_called_with(
            'The extraction order #{order_id} "Neverland" has failed. Please try again later.'.format(
                order_id=self.extraction_order.id,
            )
        )
        expected_body = '\n'.join(
            [
                'The extraction order #{order_id} "Neverland" could not be completed, please try again later.',
                '',
                'View the order at http://testserver/orders/{order_id}'
            ]
        )
        expected_body = expected_body.format(order_id=self.extraction_order.id)
        emissary_mock.inform_mail.assert_called_with(
            subject='Extraction Order #{order_id} "Neverland" failed'.format(
                order_id=self.extraction_order.id,
            ),
            mail_body=expected_body,
        )

    def tearDown(self):
        if os.path.isdir(settings.PRIVATE_MEDIA_ROOT):
            shutil.rmtree(settings.PRIVATE_MEDIA_ROOT)


class OrderUpdaterMiddlewareTest(TestCase):
    @patch('osmaxx.job_progress.middleware.update_orders_of_request_user')
    def test_request_middleware_updates_orders_of_request_user(self, update_orders_mock):
        self.client.get('/dummy/')
        update_orders_mock.assert_called_once_with(ANY)

    @patch('osmaxx.job_progress.middleware.update_orders_of_request_user')
    def test_request_middleware_passes_request_with_user(self, update_orders_mock):
        self.client.get('/dummy/')
        args, kwargs = update_orders_mock.call_args
        request = args[0]
        self.assertIsNotNone(request.build_absolute_uri.__call__, msg='not a usable request')
        self.assertIsNotNone(request.user)

    @patch('osmaxx.job_progress.middleware.update_orders_of_request_user')
    def test_request_middleware_when_authenticated_passes_request_with_logged_in_user(self, update_orders_mock):
        user = User.objects.create_user('user', 'user@example.com', 'pw')
        self.client.login(username='user', password='pw')
        self.client.get('/dummy/')
        args, kwargs = update_orders_mock.call_args
        request = args[0]
        self.assertIsNotNone(request.build_absolute_uri.__call__, msg='not a usable request')
        self.assertEqual(user, request.user)


class OrderUpdateTest(TestCase):
    def setUp(self):
        number_of_own_orders = 2
        number_of_foreign_orders = 4
        test_user = User.objects.create_user('user', 'user@example.com', 'pw')
        other_user = User.objects.create_user('other', 'other@example.com', 'pw')
        self.own_unfinished_orders = [
            ExtractionOrder.objects.create(orderer=test_user) for i in range(number_of_own_orders)]
        own_successfully_finished_orders = [  # noqa "unused" (but needed)
            ExtractionOrder.objects.create(orderer=test_user, state=ExtractionOrderState.FINISHED) for i in range(8)
        ]
        own_failed_orders = [  # noqa "unused" (but needed)
            ExtractionOrder.objects.create(orderer=test_user, state=ExtractionOrderState.FAILED) for i in range(16)
        ]
        own_aborted_orders = [  # noqa "unused" (but needed)
            ExtractionOrder.objects.create(orderer=test_user, state=ExtractionOrderState.CANCELED) for i in range(32)
        ]
        foreign_orders = [  # noqa "unused" (but needed)
            ExtractionOrder.objects.create(orderer=other_user) for i in range(number_of_foreign_orders)
        ]
        self.client.login(username='user', password='pw')

    @patch('osmaxx.job_progress.middleware.update_order')
    def test_update_orders_of_request_user_updates_each_unfinished_order_of_request_user(self, update_progress_mock):
        self.client.get('/dummy/')
        update_progress_mock.assert_has_calls(
            [call(order) for order in self.own_unfinished_orders],
            any_order=True,
        )

    @patch('osmaxx.job_progress.middleware.update_order')
    def test_update_orders_of_request_user_does_not_update_any_orders_of_other_users_nor_own_orders_in_a_final_state(
            self, update_progress_mock
    ):
        self.client.get('/dummy/')
        self.assertEqual(update_progress_mock.call_count, len(self.own_unfinished_orders))
