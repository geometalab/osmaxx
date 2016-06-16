import pytest as pytest
import requests

from osmaxx.api_client import ConversionApiClient


@pytest.fixture
def export_with_job(export):
    export.conversion_service_job_id = 10
    export.save()
    return export


def test_update_exports_of_request_user_sets_export_to_failed_if_not_available_on_mediator(rf, mocker, export_with_job, user):
    def side_effect_function(*args, **kwargs):
        response = mocker.Mock()
        setattr(response, 'status_code', requests.codes['not_found'])

        http_error = requests.exceptions.HTTPError(response=response)
        raise http_error

    with mocker.patch.object(ConversionApiClient, 'authorized_get'):
        with mocker.patch('osmaxx.job_progress.middleware.update_export_if_stale', side_effect=side_effect_function):
            from osmaxx.job_progress.middleware import update_exports_of_request_user
            assert export_with_job.status == export_with_job.INITIAL

            http_request_mock = rf.get('/')
            http_request_mock.user = user

            update_exports_of_request_user(http_request_mock)
            export_with_job.refresh_from_db()
            assert export_with_job.status == export_with_job.FAILED


def test_update_exports_of_request_user_does_not_change_status_when_exception_occurs(rf, mocker, export_with_job, user):
    def side_effect_function(*args, **kwargs):
        raise Exception()

    with mocker.patch.object(ConversionApiClient, 'authorized_get'):

        with mocker.patch('osmaxx.job_progress.middleware.update_export_if_stale', side_effect=side_effect_function):
            from osmaxx.job_progress.middleware import update_exports_of_request_user
            assert export_with_job.status == export_with_job.INITIAL

            http_request_mock = rf.get('/')
            http_request_mock.user = user

            update_exports_of_request_user(http_request_mock)
            export_with_job.refresh_from_db()

            assert export_with_job.status == export_with_job.INITIAL
