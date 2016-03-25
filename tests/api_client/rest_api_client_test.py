import requests_mock as requests_mock_package

from osmaxx.api_client.API_client import RESTApiJWTClient


def test_get_performs_request():
    with requests_mock_package.mock() as requests_mock:
        requests_mock.get(
            # Expected request:
            'http://example.com/service/uri_base/get/example',
            request_headers={'Content-Type': 'application/json; charset=UTF-8'},

            # Response if request matched:
            json={'some response': 'you got it'}
        )
        c = RESTApiJWTClient('http://example.com/service/uri_base/')
        response = c.get('get/example')
        assert response.json() == {'some response': 'you got it'}
