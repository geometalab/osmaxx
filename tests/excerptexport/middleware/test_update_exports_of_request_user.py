import pytest
import requests

from osmaxx.api_client import ConversionApiClient
from osmaxx.conversion.constants import status


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
            assert export_with_job.status is None

            http_request_mock = rf.get('/')
            http_request_mock.user = user

            update_exports_of_request_user(http_request_mock)
            export_with_job.refresh_from_db()
            assert export_with_job.status == status.FAILED


def test_update_exports_of_request_user_does_not_change_status_when_exception_occurs(rf, mocker, export_with_job, user):
    def side_effect_function(*args, **kwargs):
        raise Exception()

    with mocker.patch.object(ConversionApiClient, 'authorized_get'):

        with mocker.patch('osmaxx.job_progress.middleware.update_export_if_stale', side_effect=side_effect_function):
            from osmaxx.job_progress.middleware import update_exports_of_request_user
            assert export_with_job.status is None

            http_request_mock = rf.get('/')
            http_request_mock.user = user

            update_exports_of_request_user(http_request_mock)
            export_with_job.refresh_from_db()

            assert export_with_job.status is None


def test_update_exports_of_request_user_sets_export_to_failed_if_status_is_overdue(rf, mocker, export, user):

    from osmaxx.excerptexport._settings import EXTRACTION_PROCESSING_TIMEOUT_TIMEDELTA
    from django.utils import timezone
    now = timezone.now()
    future = now + EXTRACTION_PROCESSING_TIMEOUT_TIMEDELTA * 2

    def side_effect_function(*args, **kwargs):
        response = mocker.Mock()
        setattr(response, 'status_code', requests.codes['gateway_timeout'])

        http_error = requests.exceptions.HTTPError(response=response)
        raise http_error

    with mocker.patch('osmaxx.excerptexport.models.export.timezone.now', side_effect=[now, future, future]):
        export.save()
        with mocker.patch.object(ConversionApiClient, 'authorized_get'):
            with mocker.patch('osmaxx.job_progress.middleware.update_export_if_stale', side_effect=side_effect_function):
                from osmaxx.job_progress.middleware import update_exports_of_request_user
                assert export.status is None

                http_request_mock = rf.get('/')
                http_request_mock.user = user

                update_exports_of_request_user(http_request_mock)
                export.refresh_from_db()
                assert export.status == status.FAILED
