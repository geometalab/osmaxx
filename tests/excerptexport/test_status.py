from unittest.mock import patch

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, BBoxBoundingGeometry
from osmaxx.excerptexport.models.extraction_order import ExtractionOrderState
from .permission_test_helper import PermissionHelperMixin
from tests.test_helpers import vcr_explicit_path as vcr


@patch('osmaxx.job_progress.middleware.update_order')
class StatusTestCase(TestCase, PermissionHelperMixin):
    extraction_order = None

    def setUp(self):
        self.user = user = User.objects.create_user('user', 'user@example.com', 'pw')
        self.client.login(username='user', password='pw')

        bounding_geometry = BBoxBoundingGeometry.create_from_bounding_box_coordinates(48, 9, 46, 6)
        bounding_geometry.save()

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

    def test_permission_denied_if_lacking_permissions(self, *args):
        response = self.client.get(
            reverse(
                'excerptexport:status',
                kwargs={'extraction_order_id': self.extraction_order.id}
            )
        )
        # redirect to 'Access Denied' page
        self.assertEqual(response.status_code, 302)

    @vcr.use_cassette('fixtures/vcr/conversion_api-StatusTestCase-test_extraction_order_status_initialized.yml')
    def test_extraction_order_status_initialized(self, *args):
        self.add_permissions_to_user()
        response = self.client.get(reverse(
            'excerptexport:status',
            kwargs={'extraction_order_id': self.extraction_order.id}
        ), HTTP_HOST='thehost.example.com')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['extraction_order'], self.extraction_order)
        self.assertContains(response, 'initialized')

    @vcr.use_cassette('fixtures/vcr/conversion_api-StatusTestCase-test_extraction_order_status_finished.yml')
    def test_extraction_order_status_finished(self, *args):
        self.add_permissions_to_user()
        self.extraction_order.state = ExtractionOrderState.FINISHED
        self.extraction_order.save()

        response = self.client.get(reverse(
            'excerptexport:status',
            kwargs={'extraction_order_id': self.extraction_order.id}
        ), HTTP_HOST='thehost.example.com')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['extraction_order'], self.extraction_order)
        self.assertContains(response, 'finished')

    def test_extraction_order_id_not_existing(self, *args):
        self.add_permissions_to_user()
        response = self.client.get(reverse(
            'excerptexport:status',
            kwargs={'extraction_order_id': 9999999999})
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse('extraction_order' in response.context)

    def test_foreign_extraction_order(self, *args):
        self.add_permissions_to_user()
        response = self.client.get(reverse(
            'excerptexport:status',
            kwargs={'extraction_order_id': self.foreign_extraction_order.id}
        ), HTTP_HOST='thehost.example.com')

        self.assertEqual(response.status_code, 403)
        self.assertIsNone(response.context)
