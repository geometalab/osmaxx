from osmaxx.api_client.API_client import RESTApiClient
from requests_mock import ANY


def test_get_requests_combined_url(requests_mock):
    """
    The requested URL is the concatenation of
    the service_base of the RESTApiClient instance and
    the relative URL passed to RESTApiClient.get().
    """
    requests_mock.get(ANY)
    c = RESTApiClient('http://example.com/service/uri_base/')
    response = c.get('get/example')
    assert response.request.url == 'http://example.com/service/uri_base/get/example'


def test_get_specifies_body_content_type(requests_mock):
    # FIXME: Does this make any sense?
    # As far as I can tell, the 'Content-Type' in the request headers specifies
    # the content type of the body of the request, not of the body of the response.
    # While GET requests can have a body (which the server should ignore if present),
    # we don't send a body in the request. Specifying an absent body's content type
    # seems rather nonsensical.
    requests_mock.get(ANY)
    c = RESTApiClient('http://example.com/service/uri_base/')
    response = c.get('get/example')
    assert response.request.headers['Content-Type'] == 'application/json; charset=UTF-8'


def test_get_sends_payload_in_query_string(requests_mock):
    requests_mock.get(ANY)
    c = RESTApiClient('http://example.com/service/uri_base/')
    response = c.get('get/example', params={'some_key': b'a value'})
    assert response.request.url == 'http://example.com/service/uri_base/get/example?some_key=a+value'


def test_get_returns_received_response(requests_mock):
    requests_mock.get(ANY, json={'some response': 'you got it'})
    c = RESTApiClient('http://example.com/service/uri_base/')
    response = c.get('get/example')
    assert response.json() == {'some response': 'you got it'}


def test_post_requests_combined_url(requests_mock):
    """
    The requested URL is the concatenation of
    the service_base of the RESTApiClient instance and
    the relative URL passed to RESTApiClient.get().
    """
    requests_mock.post(ANY)
    c = RESTApiClient('http://example.com/service/uri_base/')
    response = c.post('post/example', json_data={'pay': 'load'})
    assert response.request.url == 'http://example.com/service/uri_base/post/example'


def test_post_specifies_body_content_type(requests_mock):
    requests_mock.post(ANY)
    c = RESTApiClient('http://example.com/service/uri_base/')
    response = c.post('post/example', json_data={'pay': 'load'})
    assert response.request.headers['Content-Type'] == 'application/json; charset=UTF-8'


def test_post_sends_payload_as_json_body(requests_mock):
    requests_mock.post(ANY)
    c = RESTApiClient('http://example.com/service/uri_base/')
    response = c.post('post/example', json_data={'pay': 'load'})
    assert response.request.json() == {'pay': 'load'}


def test_post_returns_received_response(requests_mock):
    requests_mock.post(ANY, json={'some response': 'you posted it'})
    c = RESTApiClient('http://example.com/service/uri_base/')
    response = c.post('post/example', json_data={'pay': 'load'})
    assert response.json() == {'some response': 'you posted it'}
