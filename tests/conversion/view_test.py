import pytest
from rest_framework.reverse import reverse

from osmaxx.conversion import status

authenticated_access_urls = [
    reverse('clipping_area-list'),
    reverse('conversion_job-list'),
    reverse('conversion_parametrization-list'),
]


@pytest.fixture(params=authenticated_access_urls)
def access_url(request):
    return request.param


def test_access_for_unauthorized_user_denied(client, access_url):
    response = client.get(access_url)
    assert response.status_code == 403


@pytest.mark.django_db()
def test_access_for_authenticated_client_allowed(authenticated_client, access_url):
    response = authenticated_client.get(access_url)
    assert response.status_code == 200


def test_access_for_admin_user_allowed(admin_client, access_url):
    response = admin_client.get(access_url)
    assert response.status_code == 200


@pytest.mark.django_db()
def test_conversion_parametrization_creation_success(authenticated_api_client, conversion_parametrization_data):
    response = authenticated_api_client.post(reverse('conversion_parametrization-list'), conversion_parametrization_data, format='json')
    assert response.status_code == 201


@pytest.mark.django_db()
def test_conversion_parametrization_creation_fails(api_client, conversion_parametrization_data):
    response = api_client.post(reverse('conversion_parametrization-list'), conversion_parametrization_data, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_conversion_parametrization_detail_access_success(authenticated_api_client, conversion_parametrization, persisted_valid_clipping_area):
    response = authenticated_api_client.get(reverse('conversion_parametrization-detail', kwargs={'pk': conversion_parametrization.id}))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == conversion_parametrization.id
    assert data['out_format'] == conversion_parametrization.out_format
    assert data['out_srs'] == conversion_parametrization.out_srs
    assert data['clipping_area'] == persisted_valid_clipping_area.id


@pytest.mark.django_db()
def test_conversion_parametrization_detail_access_fails(api_client, conversion_parametrization):
    response = api_client.get(reverse('conversion_parametrization-detail', kwargs={'pk': conversion_parametrization.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_conversion_job_creation_success(authenticated_api_client, conversion_job_data, mocker):
    start_conversion_mock = mocker.patch('osmaxx.conversion.models.Job.start_conversion')
    response = authenticated_api_client.post(reverse('conversion_job-list'), conversion_job_data, format='json')
    data = response.json()
    assert response.status_code == 201
    assert data['callback_url'] == conversion_job_data['callback_url']
    assert data['parametrization'] == conversion_job_data['parametrization']
    assert start_conversion_mock.call_count == 1


@pytest.mark.django_db()
def test_conversion_job_creation_fails(api_client, conversion_job_data):
    response = api_client.post(reverse('conversion_job-list'), conversion_job_data, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_conversion_job_detail_access_success(authenticated_api_client, conversion_job, conversion_parametrization):
    response = authenticated_api_client.get(reverse('conversion_job-detail', kwargs={'pk': conversion_job.id}))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == conversion_job.id
    assert data['callback_url'] == conversion_job.callback_url
    assert data['parametrization'] == conversion_parametrization.id
    assert data['status'] == status.RECEIVED
    assert data['resulting_file_path'] is None


@pytest.mark.django_db()
def test_conversion_job_detail_access_fails_with_anonymous_user(api_client, conversion_job):
    response = api_client.get(reverse('conversion_job-detail', kwargs={'pk': conversion_job.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_conversion_job_absolute_url_resolves_correct(conversion_job, server_url):
    url = server_url + reverse('conversion_job-detail', kwargs={'pk': conversion_job.id})
    assert conversion_job.get_absolute_url() == url


@pytest.mark.django_db()
def test_conversion_job_creation_enqueues(authenticated_api_client, conversion_job_data, rq_mock_return, mocker):
    conversion_start_start_format_extraction_mock = mocker.patch('osmaxx.conversion.converters.converter.rq_enqueue_with_settings', return_value=rq_mock_return())
    authenticated_api_client.post(reverse('conversion_job-list'), conversion_job_data, format='json')
    assert conversion_start_start_format_extraction_mock.call_count == 1
