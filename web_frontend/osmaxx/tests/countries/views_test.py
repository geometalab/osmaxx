import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from osmaxx.countries.models import Country


@pytest.mark.django_db
def test_list_countries_contains_only_name_and_id(authenticated_client):
    # only monaco will be available in countries for testing
    assert Country.objects.count() == 1

    url = reverse('country-list')
    response = authenticated_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK

    assert response.data[0].get('name') is not None
    assert response.data[0].get('id') is not None
    assert response.data[0].get('simplified_polygon') is None


@pytest.mark.django_db
def test_detail_country_contains_simplified_polygon(authenticated_client):
    # only monaco will be available in countries for testing
    assert Country.objects.count() == 1

    country = Country.objects.first()
    url = reverse('country-detail', kwargs=dict(pk=country.id))
    response = authenticated_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK

    assert response.data.get('name') is not None
    assert response.data.get('id') is not None
    assert response.data.get('simplified_polygon') is not None
