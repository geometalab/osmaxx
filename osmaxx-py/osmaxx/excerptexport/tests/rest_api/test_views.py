import json
from unittest.mock import patch

from django.test import TestCase
from osmaxx.excerptexport.rest_api import views as api_views
from rest_framework.test import APIRequestFactory


class EstimatedFileSizeViewTests(TestCase):
    def setUp(self):
        p = patch('osmaxx.excerptexport.services.conversion_api_client.ConversionApiClient')
        self.addCleanup(p.stop)
        api_client_class_mock = p.start()

        api_client_instance_mock = api_client_class_mock.return_value
        self.estimated_file_size_api_client_mock = api_client_instance_mock.estimated_file_size
        self.estimated_file_size_api_client_mock.return_value = 'estimated_size_value'

        self.bbox_edges = {bound: "{0}_value".format(bound) for bound in ['west', 'south', 'east', 'north']}

        factory = APIRequestFactory()
        self.request = factory.get('/estimated_file_size/', self.bbox_edges)

    def test_estimated_file_size_view_calls_api_client_with_boundaries(self):
        api_views.estimated_file_size(self.request)
        self.estimated_file_size_api_client_mock.assert_called_with(**self.bbox_edges)

    def test_estimated_file_size_view_returns_response_with_size_returned_by_api_client(self):
        response = api_views.estimated_file_size(self.request)
        self.assertContains(response, json.dumps(self.estimated_file_size_api_client_mock.return_value))
