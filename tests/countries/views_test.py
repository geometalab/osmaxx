import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from osmaxx.countries.models import Country


@pytest.mark.django_db
def test_country_detail_contains_simplified_polygon(authenticated_client):
    # Only Monaco will be available in countries for testing.
    assert Country.objects.count() == 1

    country = Country.objects.first()
    url = reverse('excerptexport_api:country-detail', kwargs=dict(pk=country.id))
    response = authenticated_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data.get('type') == "Feature"
    assert data.get('id') == country.id
    assert data.get('geometry') is not None
