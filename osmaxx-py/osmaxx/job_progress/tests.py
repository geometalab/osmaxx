import json
from unittest.mock import patch

import requests_mock
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
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

    @patch('osmaxx.excerptexport.services.conversion_api_client.ConversionApiClient.login', return_value=True)
    @patch.object(ConversionApiClient, 'authorized_get', ConversionApiClient.get)  # circumvent authorization logic
    @requests_mock.Mocker(kw='requests')
    def test_calling_tracker_when_status_query_indicates_started_updates_extraction_order_state(self, *args, **mocks):
        requests_mock = mocks['requests']
        requests_mock.get(
            'http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/',
            text=json.dumps({
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
            })
        )

        factory = APIRequestFactory()
        request = factory.get(
            reverse('job_progress:tracker', kwargs=dict(order_id=self.extraction_order.id)),
            data=dict(status='http://localhost:8901/api/conversion_result/53880847-faa9-43eb-ae84-dd92f3803a28/')
        )

        views.tracker(request, order_id=self.extraction_order.id)
        self.extraction_order.refresh_from_db()
        self.assertEqual(self.extraction_order.state, ExtractionOrderState.PROCESSING)
