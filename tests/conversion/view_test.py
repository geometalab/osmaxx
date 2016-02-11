import pytest
from rest_framework.reverse import reverse

authenticated_access_urls = [
    reverse('clipping_area-list'),
    reverse('conversion_job-list'),
    reverse('conversion_parametrization-list'),
]


@pytest.fixture(params=authenticated_access_urls)
def access_urls(request):
    return request.param


def test_access_for_unauthorized_user_denied(client, access_urls):
    response = client.get(access_urls)
    assert response.status_code == 403


def test_access_for_admin_user_allowed(admin_client, access_urls):
    response = admin_client.get(access_urls)
    assert response.status_code == 200
