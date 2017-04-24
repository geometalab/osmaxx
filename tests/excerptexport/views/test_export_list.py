from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.gis import geos
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from osmaxx.excerptexport.models import Excerpt, ExtractionOrder
from tests.excerptexport.permission_test_helper import PermissionHelperMixin


# TODO: test more possibilities
@override_settings(LOGIN_URL='/login/')
@patch('osmaxx.job_progress.middleware.update_export')
class ExportListTestCase(TestCase, PermissionHelperMixin):
    extraction_order = None

    def setUp(self):
        self.user = user = User.objects.create_user('user', 'user@example.com', 'pw')

        # FIXME: use the bounding_geometry fixture for this
        bounding_geometry = geos.GEOSGeometry(
            '{"type":"MultiPolygon","coordinates":[[[[8.815935552120209,47.222220486817676],[8.815935552120209,47.22402752311505],[8.818982541561127,47.22402752311505],[8.818982541561127,47.222220486817676],[8.815935552120209,47.222220486817676]]]]}'
        )

        excerpt = Excerpt.objects.create(
            name="Switzerland",
            is_active=True,
            is_public=True,
            bounding_geometry=bounding_geometry,
            owner=user
        )

        self.extraction_order = ExtractionOrder.objects.create(
            excerpt=excerpt,
            orderer=user
        )

        self.foreign_extraction_order = ExtractionOrder.objects.create(
            excerpt=excerpt,
            orderer=User.objects.create_user('another_user', 'someone_else@example.com', 'top secret')
        )

    def test_redirect_to_login_if_not_logged_in(self, *args):
        response = self.client.get(
            reverse(
                'excerptexport:export_list'
            )
        )
        self.assertRedirects(response, '/login/?next=/exports/', fetch_redirect_response=False)

    def test_access_ok_even_without_confirmed_email(self, *args):
        self.client.login(username='user', password='pw')

        response = self.client.get(
            reverse(
                'excerptexport:export_list'
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_access_ok_with_confirmed_email_address(self, *args):
        self.client.login(username='user', password='pw')

        self.add_valid_email()
        response = self.client.get(
            reverse(
                'excerptexport:export_list'
            )
        )
        self.assertEqual(response.status_code, 200)
