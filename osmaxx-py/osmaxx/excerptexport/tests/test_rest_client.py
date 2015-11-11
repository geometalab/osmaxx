import json
from unittest import mock
from .copying_mock import CopyingMock
from requests.models import Response

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from osmaxx.excerptexport.api_client import RestClient
from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, ExtractionOrderState, BBoxBoundingGeometry


class RestClientTestCase(TestCase):
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
            'gis': {
                'formats': ['fgdb', 'spatialite'],
                'options': {
                    'coordinate_reference_system': 'WGS_84',
                    'detail_level': 1
                }
            }
        }

    def test_successful_login(self):
        response = Response()
        response.status_code = 200
        response.reason = 'OK'
        response.headers = {'content-type': 'application/json'}
        response.json = CopyingMock(return_value={'token': 'abcdefgh12345678'})
        response_mock_factory = CopyingMock(return_value=response)

        with mock.patch('requests.post', new=response_mock_factory) as request_post_mock:
            rest_client = RestClient(
                'http', 'www.osmaxx.ch', '8000',
                {'login': '/api/token-auth/?format=json'},
                {'username': 'osmaxxi', 'password': '12345678'}
            )
            self.assertFalse(rest_client.is_logged_in)

            status = rest_client.login()

            request_post_mock.assert_called_with(
                'http://www.osmaxx.ch:8000/api/token-auth/?format=json',
                data=json.dumps({'username': 'osmaxxi', 'password': '12345678'}),
                headers={'Content-Type': 'application/json; charset=UTF-8'}
            )

            self.assertTrue(status)
            self.assertTrue(rest_client.is_logged_in)
            self.assertEqual(rest_client.headers['Authorization'], 'JWT abcdefgh12345678')

    def test_failed_login(self):
        response = Response()
        response.status_code = 400
        response.reason = 'BAD REQUEST'
        response.headers = {'content-type': 'application/json'}
        response.json = CopyingMock(return_value={'non_field_errors': ['Unable to login with provided credentials.']})
        response_mock_factory = CopyingMock(return_value=response)

        with mock.patch('requests.post', new=response_mock_factory) as request_post_mock:
            rest_client = RestClient(
                'http', 'www.osmaxx.ch', '8000',
                {'login': '/api/token-auth/?format=json'},
                {'username': 'osmaxxi', 'password': 'wrong-password'}
            )
            self.assertFalse(rest_client.is_logged_in)

            status = rest_client.login()

            request_post_mock.assert_called_with(
                'http://www.osmaxx.ch:8000/api/token-auth/?format=json',
                data=json.dumps({'username': 'osmaxxi', 'password': 'wrong-password'}),
                headers={'Content-Type': 'application/json; charset=UTF-8'}
            )

            self.assertFalse(status)
            self.assertFalse(rest_client.is_logged_in)
            self.assertFalse('Authorization' in rest_client.headers)

    def test_create_job(self):
        response = Response()
        response.status_code = 200
        response.reason = 'OK'
        response.headers = {'content-type': 'application/json'}
        response.json = CopyingMock(return_value={
            "id": 5,
            "rq_job_id": "81cca3a9-5e66-47ab-8d3f-70739e4204ae",
            "callback_url": "http://example.com",
            "status": "http://localhost:9000/api/conversion_result/81cca3a9-5e66-47ab-8d3f-70739e4204ae/",
            "gis_formats": [
                "fgdb",
                "spatialite"
            ],
            "gis_options": {
                "coordinate_reference_system": "WGS_84",
                "detail_level": 1
            },
            "extent": {
                "id": 5,
                "west": 29.525547623634335,
                "south": 40.77546776498174,
                "east": 29.528980851173397,
                "north": 40.77739734768811,
                "polyfile": None
            }
        })
        response_mock_factory = CopyingMock(return_value=response)
        with mock.patch('requests.post', new=response_mock_factory) as request_post_mock:
            rest_client = RestClient(
                'http', 'www.osmaxx.ch', '8000',
                {'job': {'create': '/api/jobs'}},
                {'username': 'osmaxxi', 'password': '12345678'}
            )
            rest_client.is_logged_in = True
            rest_client.headers['Authorization'] = 'JWT abcdefgh12345678'

            status = rest_client.create_job(self.extraction_order)

            request_post_mock.assert_called_with(
                'http://www.osmaxx.ch:8000/api/jobs',
                data=json.dumps({
                    "callback_url": "http://example.com",
                    "gis_formats": ["fgdb", "spatialite"],
                    "gis_options": {
                        "coordinate_reference_system": "WGS_84",
                        "detail_level": 1
                    },
                    "extent": {
                        "west": 29.525547623634335,
                        "south": 40.77546776498174,
                        "east": 29.528980851173397,
                        "north": 40.77739734768811,
                        "polyfile": None
                    }
                }),
                headers={'Content-Type': 'application/json; charset=UTF-8', 'Authorization': 'JWT abcdefgh12345678'}
            )

            self.assertTrue(status)
            self.assertEqual(self.extraction_order.state, ExtractionOrderState.PROCESSING)
            self.assertEqual(self.extraction_order.process_id, '81cca3a9-5e66-47ab-8d3f-70739e4204ae')
