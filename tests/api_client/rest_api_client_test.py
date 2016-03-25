from osmaxx.api_client.API_client import RESTApiJWTClient
from requests_mock import ANY


def test_get_performs_request(requests_mock):
    requests_mock.get(
        # Expected request:
        ANY,
        request_headers={'Content-Type': 'application/json; charset=UTF-8'},

        # Response if request matched:
        json={'some response': 'you got it'}
    )
    c = RESTApiJWTClient('http://example.com/service/uri_base/')
    response = c.get('get/example')
    assert response.request.url == 'http://example.com/service/uri_base/get/example'
    assert response.json() == {'some response': 'you got it'}


def test_post_performs_request(requests_mock):
    requests_mock.post(
        # Expected request:
        ANY,
        request_headers={'Content-Type': 'application/json; charset=UTF-8'},

        # Response if request matched:
        json={'some response': 'you posted it'}
    )
    c = RESTApiJWTClient('http://example.com/service/uri_base/')
    response = c.post('post/example', json_data={'pay': 'load'})
    assert response.request.url == 'http://example.com/service/uri_base/post/example'
    assert response.request.json() == {'pay': 'load'}
    assert response.json() == {'some response': 'you posted it'}
