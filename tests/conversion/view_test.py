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
