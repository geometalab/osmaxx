from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from excerptexport.models import Excerpt, ExtractionOrder, BoundingGeometry
from excerptexport.models.extraction_order import ExtractionOrderState
from excerptexport.tests.permission_test_helper import PermissionHelperMixin


class StatusTestCase(TestCase, PermissionHelperMixin):
    extraction_order = None

    def setUp(self):
        self.user = user = User.objects.create_user('user', 'user@example.com', 'pw')
        self.client.login(username='user', password='pw')

        bounding_geometry = BoundingGeometry.create_from_bounding_box_coordinates(48, 9, 46, 6)
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

    def test_permission_denied_if_lacking_permissions(self):
        response = self.client.get(
            reverse(
                'excerptexport:status',
                kwargs={'extraction_order_id': self.extraction_order.id}
            )
        )
        # redirect to 'Access Denied' page
        self.assertEqual(response.status_code, 302)

    def test_extraction_order_status_initialized(self):
        self.add_permissions_to_user()
        response = self.client.get(reverse(
            'excerptexport:status',
            kwargs={'extraction_order_id': self.extraction_order.id}
        ), HTTP_HOST='thehost.example.com')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['extraction_order'], self.extraction_order)
        self.assertContains(response, 'initialized')

    def test_extraction_order_status_finished(self):
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

    def test_extraction_order_id_not_existing(self):
        self.add_permissions_to_user()
        response = self.client.get(reverse('excerptexport:status', kwargs={'extraction_order_id': 9999999999}))

        self.assertEqual(response.status_code, 404)
        self.assertFalse('extraction_order' in response.context)
