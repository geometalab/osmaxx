import pytest
from rest_framework.reverse import reverse

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
def test_conversion_parametrization_creation_success(api_client_authenticated, conversion_parametrization_data):
    response = api_client_authenticated.post(reverse('conversion_parametrization-list'), conversion_parametrization_data, format='json')
    assert response.status_code == 201


@pytest.mark.django_db()
def test_conversion_parametrization_creation_fails(api_client, conversion_parametrization_data):
    response = api_client.post(reverse('conversion_parametrization-list'), conversion_parametrization_data, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_conversion_parametrization_detail_access_success(api_client_authenticated, conversion_parametrization, valid_clipping_area):
    response = api_client_authenticated.get(reverse('conversion_parametrization-detail', kwargs={'pk': conversion_parametrization.id}))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == conversion_parametrization.id
    assert data['out_format'] == conversion_parametrization.out_format
    assert data['out_srs'] == conversion_parametrization.out_srs
    assert data['clipping_area'] == valid_clipping_area.id


@pytest.mark.django_db()
def test_conversion_parametrization_detail_access_fails(api_client, conversion_parametrization):
    response = api_client.get(reverse('conversion_parametrization-detail', kwargs={'pk': conversion_parametrization.id}))
    assert response.status_code == 403
