from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from osmaxx.countries.models import Country


class AccountTests(APITestCase):
    def test_list_countries_contains_only_name_and_id(self):
        # only monaco will be available in countries for testing
        self.assertEqual(Country.objects.count(), 1)

        user = User.objects.create_user(username='lauren', password='lauri', email=None)
        self.client.force_authenticate(user=user)

        url = reverse('country-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNotNone(response.data[0].get('name'))
        self.assertIsNotNone(response.data[0].get('id'))
        self.assertIsNone(response.data[0].get('simplified_polygon'))

    def test_detail_country_contains_simplified_polygon(self):
        # only monaco will be available in countries for testing
        self.assertEqual(Country.objects.count(), 1)

        user = User.objects.create_user(username='lauren', password='lauri', email=None)
        self.client.force_authenticate(user=user)

        country = Country.objects.first()
        url = reverse('country-detail', kwargs=dict(pk=country.id))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNotNone(response.data.get('name'))
        self.assertIsNotNone(response.data.get('id'))
        self.assertIsNotNone(response.data.get('simplified_polygon'))
