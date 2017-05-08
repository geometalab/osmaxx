from unittest import mock
from unittest.mock import Mock, sentinel, ANY
from urllib.parse import urlparse

import pytest
from django.core.urlresolvers import resolve
from hamcrest import assert_that, contains_inanyorder
from requests import HTTPError
from rest_framework.reverse import reverse

from osmaxx.api_client import ConversionApiClient, API_client
from osmaxx.conversion.constants.formats import FGDB, SPATIALITE
from osmaxx.conversion.constants.statuses import RECEIVED
from osmaxx.excerptexport.models import Excerpt, ExtractionOrder
from osmaxx.job_progress.views import tracker
from tests.test_helpers import vcr_explicit_path as vcr


# Authentication tests

@vcr.use_cassette('fixtures/vcr/conversion_api-test_successful_login.yml')
def test_successful_login():
    api_client = ConversionApiClient()

    assert api_client.token is None

    api_client._login()

    assert api_client.token is not None


@vcr.use_cassette('fixtures/vcr/conversion_api-test_failed_login.yml')
def test_failed_login():
    api_client = ConversionApiClient()
    api_client.password = 'invalid'

    assert api_client.password == 'invalid'
    assert api_client.token is None

    expected_msg = \
        "400 Client Error: Bad Request for url: http://localhost:8901/api/token-auth/"
    with pytest.raises(HTTPError) as excinfo:
        api_client._login()

    assert str(excinfo.value) == expected_msg
    assert API_client.reasons_for(excinfo.value) == {'non_field_errors': ['Unable to login with provided credentials.']}
    assert api_client.token is None


@pytest.fixture
def the_host():
    return "the-host.example.com"


@pytest.fixture
def job_progress_request(the_host):
    request = Mock()
    request.build_absolute_uri.return_value = 'http://' + the_host + '/job_progress/tracker/23/'
    return request


@pytest.fixture
def excerpt_request(the_host):
    request = Mock()
    request.build_absolute_uri.return_value = 'http://' + the_host + '/orders/new/new_excerpt/'
    return request


@pytest.fixture
def excerpt(user, bounding_geometry, db):
    return Excerpt.objects.create(
        name='Neverland', is_active=True, is_public=True, owner=user, bounding_geometry=bounding_geometry
    )


@pytest.fixture
def extraction_order(excerpt, user, db):
    extraction_order = ExtractionOrder.objects.create(excerpt=excerpt, orderer=user, id=23)
    extraction_order.extraction_formats = [FGDB, SPATIALITE]
    extraction_order.coordinate_reference_system = 4326
    return extraction_order


#
# ConversionApiClient unit tests:

def test_extraction_order_forward_to_conversion_service(
        rf, mocker, excerpt, extraction_order, bounding_geometry, the_host):
    mocker.patch.object(
        ConversionApiClient, 'create_job',
        side_effect=[{'id': 5, 'status': RECEIVED}, {'id': 23, 'status': RECEIVED}],
    )
    mocker.patch.object(
        ConversionApiClient, 'create_parametrization',
        side_effect=[sentinel.parametrization_1, sentinel.parametrization_2],
    )
    mocker.patch.object(ConversionApiClient, 'create_boundary')

    request = rf.get('/tracker/something', HTTP_HOST=the_host)
    result = extraction_order.forward_to_conversion_service(incoming_request=request)

    ConversionApiClient.create_boundary.assert_called_once_with(bounding_geometry, name=excerpt.name)
    srs = extraction_order.coordinate_reference_system
    detail_level = extraction_order.detail_level
    assert_that(
        ConversionApiClient.create_parametrization.mock_calls, contains_inanyorder(
            mock.call(boundary=ConversionApiClient.create_boundary.return_value, out_format=FGDB, detail_level=detail_level, out_srs=srs),
            mock.call(boundary=ConversionApiClient.create_boundary.return_value, out_format=SPATIALITE, detail_level=detail_level, out_srs=srs),
        )
    )
    assert_that(
        ConversionApiClient.create_job.mock_calls, contains_inanyorder(
            mock.call(sentinel.parametrization_1, ANY, user=ANY),
            mock.call(sentinel.parametrization_2, ANY, user=ANY),
        )
    )
    fgdb_export = extraction_order.exports.get(file_format=FGDB)
    spatialite_export = extraction_order.exports.get(file_format=SPATIALITE)
    fgdb_callback_uri_path = reverse('job_progress:tracker', kwargs=dict(export_id=fgdb_export.id))
    spatialite_callback_uri_path = reverse('job_progress:tracker', kwargs=dict(export_id=spatialite_export.id))
    assert_that(
        ConversionApiClient.create_job.mock_calls, contains_inanyorder(
            mock.call(ANY, 'http://' + the_host + fgdb_callback_uri_path, user=ANY),
            mock.call(ANY, 'http://' + the_host + spatialite_callback_uri_path, user=ANY),
        )
    )
    assert_that(
        result, contains_inanyorder(
            {'id': 5, 'status': 'received'},
            {'id': 23, 'status': 'received'},
        )
    )
    assert_that(
        extraction_order.exports.values_list('file_format', flat=True), contains_inanyorder(
            FGDB,
            SPATIALITE,
        )
    )
    assert_that(
        extraction_order.exports.values_list('conversion_service_job_id', flat=True), contains_inanyorder(
            5,
            23,
        )
    )


@pytest.fixture
def api_client():
    return ConversionApiClient()


#
# ConversionApiClient integration tests:

@vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job.yml')
def test_create_jobs_for_extraction_order(extraction_order, excerpt_request):
    fgdb_export = extraction_order.exports.get(file_format=FGDB)
    spatialite_export = extraction_order.exports.get(file_format=SPATIALITE)

    assert fgdb_export.conversion_service_job_id is None
    assert fgdb_export.status == fgdb_export.INITIAL
    assert spatialite_export.conversion_service_job_id is None
    assert spatialite_export.status == spatialite_export.INITIAL

    jobs_json = extraction_order.forward_to_conversion_service(incoming_request=(excerpt_request))

    fgdb_export.refresh_from_db()
    spatialite_export.refresh_from_db()

    assert fgdb_export.status == RECEIVED
    assert spatialite_export.status == RECEIVED
    assert len(jobs_json) == 2
    for job_json in jobs_json:
        expected_keys_in_response = ['callback_url', 'rq_job_id', 'id', 'status', 'resulting_file', 'parametrization']
        actual_keys_in_response = job_json.keys()
        assert_that(expected_keys_in_response, contains_inanyorder(*actual_keys_in_response))


@pytest.fixture
def clipping_area_json():
    return {
        "id": 17,
        "name": "Neverland",
        "clipping_multi_polygon": {
            "type": "MultiPolygon",
            "coordinates": [[[
                [29.525547623634335, 40.77546776498174],
                [29.525547623634335, 40.77739734768811],
                [29.528980851173397, 40.77739734768811],
                [29.528980851173397, 40.77546776498174],
                [29.525547623634335, 40.77546776498174],
            ]]],
        }
    }


@vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job_for_export.yml')
def test_create_job_for_export(extraction_order, job_progress_request, clipping_area_json):
    fgdb_export = extraction_order.exports.get(file_format=FGDB)
    job_json = fgdb_export.send_to_conversion_service(clipping_area_json, incoming_request=job_progress_request)
    assert job_json['callback_url'] == "http://the-host.example.com/job_progress/tracker/23/"
    assert job_json['rq_job_id'] == "6692fa44-cc19-4252-88ae-8687496da421"
    assert job_json['id'] == 29
    assert job_json['status'] == RECEIVED
    assert job_json['resulting_file'] is None
    assert job_json['parametrization'] == 38


@vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job_for_export.yml')
def test_callback_url_of_created_job_refers_to_correct_export(extraction_order, job_progress_request, clipping_area_json):
    fgdb_export = extraction_order.exports.get(file_format=FGDB)

    job_json = fgdb_export.send_to_conversion_service(clipping_area_json, incoming_request=job_progress_request)

    callback_url = job_json['callback_url']
    scheme, host, callback_path, params, *_ = urlparse(callback_url)

    match = resolve(callback_path)
    assert match.func == tracker
    job_progress_request.build_absolute_uri.assert_called_with('/job_progress/tracker/{}/'.format(fgdb_export.id))


@vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job_for_export.yml')
def test_callback_url_would_reach_this_django_instance(extraction_order, job_progress_request, the_host, clipping_area_json):
    fgdb_export = extraction_order.exports.get(file_format=FGDB)

    job_json = fgdb_export.send_to_conversion_service(clipping_area_json, incoming_request=job_progress_request)

    callback_url = job_json['callback_url']
    scheme, host, callback_path, params, *_ = urlparse(callback_url)
    assert scheme.startswith('http')  # also matches https
    assert host == the_host
