import json
from unittest import mock
from .copying_mock import CopyingMock
from requests.models import Response

from django.test.testcases import TestCase

from osmaxx.excerptexport.api_client import RestClient


class RestClientTestCase(TestCase):
    result = None

    def tearDown(self):
        self.result = None

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
