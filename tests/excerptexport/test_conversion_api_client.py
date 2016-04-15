import time
from unittest import mock
from unittest.mock import Mock, sentinel
from urllib.parse import urlparse

import os

import pytest
from django.core.urlresolvers import resolve
from hamcrest import assert_that, contains_inanyorder, close_to as is_close_to
from requests import HTTPError

from osmaxx.api_client import ConversionApiClient, API_client
from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, ExtractionOrderState, BBoxBoundingGeometry
from osmaxx.job_progress.views import tracker
from tests.test_helpers import vcr_explicit_path as vcr, absolute_cassette_lib_path


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
        "400 Client Error: BAD REQUEST for url: http://localhost:8901/api/token-auth/"
    with pytest.raises(HTTPError) as excinfo:
        api_client._login()

    assert str(excinfo.value) == expected_msg
    assert API_client.reasons_for(excinfo.value) == {'non_field_errors': ['Unable to login with provided credentials.']}
    assert api_client.token is None


@pytest.fixture
def job_progress_request():
    request = Mock()
    request.build_absolute_uri.return_value = 'http://the-host.example.com/job_progress/tracker/23/'
    return request


@pytest.fixture
def bounding_box(db):
    return BBoxBoundingGeometry.create_from_bounding_box_coordinates(
        40.77739734768811, 29.528980851173397, 40.77546776498174, 29.525547623634335
    )


@pytest.fixture
def excerpt(user, bounding_box, db):
    return Excerpt.objects.create(
        name='Neverland', is_active=True, is_public=True, owner=user, bounding_geometry=bounding_box
    )


@pytest.fixture
def extraction_order(excerpt, user, db):
    extraction_order = ExtractionOrder.objects.create(excerpt=excerpt, orderer=user, id=23)
    extraction_order.extraction_formats = ['fgdb', 'spatialite']
    extraction_order.extraction_configuration = {
        'gis_options': {
            'coordinate_reference_system': 'WGS_84',
            'detail_level': 1
        }
    }
    return extraction_order


#
# ConversionApiClient unit tests:

def test_extraction_order_forward_to_conversion_service(mocker, excerpt, extraction_order, job_progress_request, bounding_box):
    mocker.patch.object(ConversionApiClient, 'create_job', side_effect=[sentinel.job_1, sentinel.job_2])
    mocker.patch.object(
        ConversionApiClient, 'create_parametrization',
        side_effect=[sentinel.parametrization_1, sentinel.parametrization_2],
    )
    mocker.patch.object(ConversionApiClient, 'create_boundary')

    result = extraction_order.forward_to_conversion_service(incoming_request=job_progress_request)

    ConversionApiClient.create_boundary.assert_called_once_with(bounding_box.geometry, name=excerpt.name)
    gis_conversion_options = extraction_order.extraction_configuration['gis_options']
    assert_that(
        ConversionApiClient.create_parametrization.mock_calls, contains_inanyorder(
            mock.call(ConversionApiClient.create_boundary.return_value, 'fgdb', gis_conversion_options),
            mock.call(ConversionApiClient.create_boundary.return_value, 'spatialite', gis_conversion_options),
        )
    )
    assert_that(
        ConversionApiClient.create_job.mock_calls, contains_inanyorder(
            # FIXME: Must be called with callback url, not with request.
            mock.call(sentinel.parametrization_1, job_progress_request),
            mock.call(sentinel.parametrization_2, job_progress_request),
        )
    )
    assert_that(
        result, contains_inanyorder(
            sentinel.job_1,
            sentinel.job_2,
        )
    )


@pytest.fixture
def api_client():
    return ConversionApiClient()


#
# ConversionApiClient integration tests:

# TODO: re-record VCR (service API has changed)

@vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job.yml')
def test_create_job(api_client, extraction_order, job_progress_request):
    assert extraction_order.process_id is None

    response = api_client._create_job_TODO_replace_me(extraction_order, request=job_progress_request)

    assert response.request.headers['Authorization'] == 'JWT {token}'.format(token=api_client.token)
    expected_keys_in_response = ["rq_job_id", "callback_url", "status", "gis_formats", "gis_options", "extent"]
    actual_keys_in_response = response.json().keys()
    assert_that(expected_keys_in_response, contains_inanyorder(*actual_keys_in_response))
    assert extraction_order.state == ExtractionOrderState.QUEUED
    assert extraction_order.process_id == response.json().get('rq_job_id')
    assert extraction_order.process_id is not None
    job_progress_request.build_absolute_uri.assert_called_with('/job_progress/tracker/23/')


@vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job.yml')  # Intentionally same as for test_create_job()
def test_callback_url_of_created_job_resolves_to_job_updater(api_client, extraction_order, job_progress_request):
    assert extraction_order.process_id is None

    response = api_client._create_job_TODO_replace_me(extraction_order, request=job_progress_request)

    callback_url = response.json()['callback_url']
    scheme, host, callback_path, params, *_ = urlparse(callback_url)

    match = resolve(callback_path)
    assert match.func == tracker
    job_progress_request.build_absolute_uri.assert_called_with('/job_progress/tracker/23/')


@vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job.yml')  # Intentionally same as for test_create_job()
def test_callback_url_of_created_job_refers_to_correct_extraction_order(api_client, extraction_order, job_progress_request):
    assert extraction_order.process_id is None

    response = api_client._create_job_TODO_replace_me(extraction_order, request=job_progress_request)

    callback_url = response.json()['callback_url']
    scheme, host, callback_path, params, *_ = urlparse(callback_url)

    match = resolve(callback_path)
    assert match.kwargs == {'order_id': str(extraction_order.id)}
    job_progress_request.build_absolute_uri.assert_called_with('/job_progress/tracker/23/')


@vcr.use_cassette('fixtures/vcr/conversion_api-test_create_job.yml')  # Intentionally same as for test_create_job()
def test_callback_url_would_reach_this_django_instance(api_client, extraction_order, job_progress_request):
    assert extraction_order.process_id is None

    response = api_client._create_job_TODO_replace_me(extraction_order, request=job_progress_request)

    callback_url = response.json()['callback_url']
    scheme, host, callback_path, params, *_ = urlparse(callback_url)
    assert scheme.startswith('http')  # also matches https
    assert host == 'the-host.example.com'
    job_progress_request.build_absolute_uri.assert_called_with('/job_progress/tracker/23/')


def test_download_files(api_client, extraction_order, job_progress_request):
    cassette_file_location = os.path.join(
        absolute_cassette_lib_path,
        'fixtures/vcr/conversion_api-test_download_files.yml'
    )
    cassette_empty = not os.path.exists(cassette_file_location)

    with vcr.use_cassette(cassette_file_location):
        api_client._create_job_TODO_replace_me(extraction_order, request=job_progress_request)

        if cassette_empty:
            # wait for external service to complete request
            time.sleep(120)

        api_client._download_result_files(
            extraction_order,
            job_status=api_client.job_status(extraction_order)
        )
        content_types_of_output_files = (f.content_type for f in extraction_order.output_files.all())
        ordered_formats = extraction_order.extraction_formats
        assert_that(content_types_of_output_files, contains_inanyorder(*ordered_formats))
        assert_that(
            len(extraction_order.output_files.order_by('id')[0].file.read()),
            is_close_to(446005, delta=10000)
        )
        assert_that(
            len(extraction_order.output_files.order_by('id')[1].file.read()),
            is_close_to(368378, delta=10000)
        )
    job_progress_request.build_absolute_uri.assert_called_with('/job_progress/tracker/23/')


def test_order_status_processing(api_client, extraction_order, job_progress_request):
    cassette_file_location = os.path.join(
        absolute_cassette_lib_path,
        'fixtures/vcr/conversion_api-test_order_status_processing.yml'
    )
    cassette_empty = not os.path.exists(cassette_file_location)
    with vcr.use_cassette(cassette_file_location):
        assert extraction_order.output_files.count() == 0
        assert extraction_order.state != ExtractionOrderState.PROCESSING
        assert extraction_order.state == ExtractionOrderState.INITIALIZED

        api_client._create_job_TODO_replace_me(extraction_order, request=job_progress_request)

        if cassette_empty:
            time.sleep(10)

        api_client.update_order_status(extraction_order)
        assert extraction_order.state == ExtractionOrderState.PROCESSING
        assert extraction_order.state != ExtractionOrderState.INITIALIZED
        assert extraction_order.output_files.count() == 0
    job_progress_request.build_absolute_uri.assert_called_with('/job_progress/tracker/23/')


def test_order_status_done(api_client, extraction_order, job_progress_request):
    cassette_file_location = os.path.join(
        absolute_cassette_lib_path,
        'fixtures/vcr/conversion_api-test_order_status_done.yml'
    )
    cassette_empty = not os.path.exists(cassette_file_location)

    with vcr.use_cassette(cassette_file_location):
        api_client._create_job_TODO_replace_me(extraction_order, request=job_progress_request)
        api_client.update_order_status(extraction_order)  # processing
        assert extraction_order.output_files.count() == 0
        assert extraction_order.state != ExtractionOrderState.FINISHED

        if cassette_empty:
            # wait for external service to complete request
            time.sleep(120)

        api_client.update_order_status(extraction_order)
        assert extraction_order.state == ExtractionOrderState.FINISHED
    job_progress_request.build_absolute_uri.assert_called_with('/job_progress/tracker/23/')
