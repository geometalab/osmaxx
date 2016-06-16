import requests

from osmaxx.api_client import ConversionApiClient


def test_update_exports_of_request_user_sets_export_to_failed_if_not_available_on_mediator(rf, mocker, export, user):
    def side_effect_function(*args, **kwargs):
        response = mocker.Mock()
        setattr(response, 'status_code', requests.codes['not_found'])

        http_error = requests.exceptions.HTTPError(response=response)
        raise http_error

    with mocker.patch.object(ConversionApiClient, 'authorized_get'):
        export.conversion_service_job_id = 10
        export.save()

        with mocker.patch('osmaxx.job_progress.middleware.update_export_if_stale', side_effect=side_effect_function):
            from osmaxx.job_progress.middleware import update_exports_of_request_user
            assert export.status == export.INITIAL

            http_request_mock = rf.get('/')
            http_request_mock.user = user

            update_exports_of_request_user(http_request_mock)
            export.refresh_from_db()
            assert export.status == export.FAILED
