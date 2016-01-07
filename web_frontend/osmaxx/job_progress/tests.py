import json
from unittest.mock import patch

import requests_mock
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import Http404
from osmaxx.excerptexport.models.bounding_geometry import BBoxBoundingGeometry
from osmaxx.excerptexport.models.excerpt import Excerpt
from osmaxx.excerptexport.models.extraction_order import ExtractionOrder, ExtractionOrderState
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
        self.fgdb_started_and_spatialite_queued_response = json.dumps(
            {
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
        )

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
            text=self.fgdb_started_and_spatialite_queued_response
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
    @patch('osmaxx.job_progress.views.Emissary.info')
    def test_calling_tracker_when_status_query_indicates_started_informs_user(self, info_mock, *args, **mocks):
        requests_mock = mocks['requests']
        requests_mock.get(
            'http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/',
            text=self.fgdb_started_and_spatialite_queued_response
        )

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(order_id=self.extraction_order.id)),
            data=dict(status='http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/')
        )

        views.tracker(request, order_id=str(self.extraction_order.id))
        info_mock.assert_called_with(
            'Extraction order {order_id} is now PROCESSING.'.format(
                order_id=self.extraction_order.id
            )
        )

    @patch('osmaxx.excerptexport.services.conversion_api_client.ConversionApiClient.login', return_value=True)
    @patch.object(ConversionApiClient, 'authorized_get', ConversionApiClient.get)  # circumvent authorization logic
    @patch('osmaxx.excerptexport.services.conversion_api_client.ConversionApiClient._download_file')  # mock download
    @requests_mock.Mocker(kw='requests')
    @patch('osmaxx.job_progress.views.Emissary.error')
    @patch('osmaxx.job_progress.views.Emissary.warn')
    @patch('osmaxx.job_progress.views.Emissary.success')
    def test_calling_tracker_when_status_query_indicates_finished_informs_user(
            self, emissary_success_mock, emissary_warn_mock, emissary_error_mock, *args, **mocks
    ):
        requests_mock = mocks['requests']
        requests_mock.get(
            'http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/',
            text=json.dumps({
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
            })
        )

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(order_id=self.extraction_order.id)),
            data=dict(status='http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/')
        )

        views.tracker(request, order_id=str(self.extraction_order.id))
        self.extraction_order.refresh_from_db()
        self.assertEqual(self.extraction_order.state, ExtractionOrderState.FINISHED)
        emissary_success_mock.assert_called_with('The extraction of the order "1" has been finished.')
        emissary_warn_mock.assert_not_called()
        emissary_error_mock.assert_not_called()

    @patch('osmaxx.excerptexport.services.conversion_api_client.ConversionApiClient.login', return_value=True)
    @patch.object(ConversionApiClient, 'authorized_get', ConversionApiClient.get)  # circumvent authorization logic
    @requests_mock.Mocker(kw='requests')
    @patch('osmaxx.job_progress.views.Emissary.error')
    @patch('osmaxx.job_progress.views.Emissary.warn')
    @patch('osmaxx.job_progress.views.Emissary.success')
    def test_calling_tracker_when_status_query_indicates_error_informs_user(
            self, emissary_success_mock, emissary_warn_mock, emissary_error_mock, *args, **mocks
    ):
        requests_mock = mocks['requests']
        requests_mock.get(
            'http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/',
            text=json.dumps({
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
            })
        )

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(order_id=self.extraction_order.id)),
            data=dict(status='http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/')
        )

        views.tracker(request, order_id=str(self.extraction_order.id))
        self.extraction_order.refresh_from_db()
        self.assertEqual(self.extraction_order.state, ExtractionOrderState.FAILED)
        emissary_success_mock.assert_not_called()
        emissary_warn_mock.assert_not_called()
        emissary_error_mock.assert_called_with('The extraction order "1" has failed. Please try again later.')
