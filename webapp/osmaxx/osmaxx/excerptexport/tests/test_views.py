from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from osmaxx.excerptexport.models import ExtractionOrder, Excerpt
from osmaxx.excerptexport.models.bounding_geometry import BoundingGeometry
from osmaxx.excerptexport.tests.permission_test_helper import PermissionHelperMixin


class ExcerptExportViewTests(TestCase, PermissionHelperMixin):
    user = None
    new_excerpt_post_data = None
    existing_excerpt = None
    existing_excerpt_post_data = None

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'pw')
        self.new_excerpt_post_data = {
            'form-mode': 'create_new_excerpt',
            'new_excerpt_name': 'A very interesting region',
            'new_excerpt_is_public': 'True',
            'new_excerpt_bounding_box_north': '1.0',
            'new_excerpt_bounding_box_east': '2.0',
            'new_excerpt_bounding_box_south': '3.0',
            'new_excerpt_bounding_box_west': '4.0'
        }
        existing_excerpt = Excerpt.objects.create(
            name='Some old Excerpt',
            is_active=True,
            is_public=False,
            owner=self.user,
            bounding_geometry=BoundingGeometry.objects.create()
        )
        self.existing_excerpt_post_data = {
            'form-mode': 'existing_excerpt',
            'existing_excerpt.id': existing_excerpt.id
        }

    def test_new_when_not_logged_in(self):
        """
        When not logged in, we get redirected.
        """
        response = self.client.get(reverse('excerptexport:new'))
        self.assertEqual(response.status_code, 302)

    def test_new(self):
        """
        When logged in, we get the excerpt choice form.
        """
        self.add_permissions_to_user()
        self.client.login(username='user', password='pw')
        response = self.client.get(reverse('excerptexport:new'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create new excerpt')

    def test_create_when_not_logged_in(self):
        """
        When not logged in, we get redirected.
        """
        response = self.client.post(reverse('excerptexport:new'), self.new_excerpt_post_data)
        self.assertEqual(response.status_code, 302)

    def test_create_with_new_excerpt(self):
        """
        When logged in, POSTing an export request with a new excerpt is successful.
        """
        self.add_permissions_to_user()
        self.client.login(username='user', password='pw')
        response = self.client.post(
            reverse('excerptexport:new'),
            self.new_excerpt_post_data,
            HTTP_HOST='thehost.example.com'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Excerpt.objects.filter(name='A very interesting region', is_active=True, is_public=True).count(),
            1
        )

    def test_create_with_existing_excerpt(self):
        """
        When logged in, POSTing an export request using an existing excerpt is successful.
        """
        self.add_permissions_to_user()
        self.client.login(username='user', password='pw')
        response = self.client.post(
            reverse('excerptexport:new'),
            self.existing_excerpt_post_data,
            HTTP_HOST='thehost.example.com'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ExtractionOrder.objects.filter(
            excerpt_id=self.existing_excerpt_post_data['existing_excerpt.id']
        ).count(), 1)  # only reproducible because there is only 1

    def test_create_with_new_excerpt_persists_a_new_order(self):
        """
        When logged in, POSTing an export request with a new excerpt persists a new ExtractionOrder.
        """
        self.add_permissions_to_user()
        self.assertEqual(ExtractionOrder.objects.count(), 0)
        self.client.login(username='user', password='pw')
        self.client.post(reverse('excerptexport:new'), self.new_excerpt_post_data, HTTP_HOST='thehost.example.com')
        self.assertEqual(ExtractionOrder.objects.count(), 1)

        newly_created_order = ExtractionOrder.objects.first()  # only reproducible because there is only 1
        from osmaxx.excerptexport.models.extraction_order import ExtractionOrderState
        self.assertEqual(newly_created_order.state, ExtractionOrderState.INITIALIZED)
        self.assertIsNone(newly_created_order.process_start_date)
        self.assertIsNone(newly_created_order.process_reference)
        self.assertEqual(newly_created_order.orderer, self.user)
        self.assertEqual(newly_created_order.excerpt.name, 'A very interesting region')

    def test_create_with_existing_excerpt_persists_a_new_order(self):
        """
        When logged in, POSTing an export request using an existing excerpt persists a new ExtractionOrder.
        """
        self.add_permissions_to_user()
        self.assertEqual(ExtractionOrder.objects.count(), 0)
        self.client.login(username='user', password='pw')
        self.client.post(
            reverse('excerptexport:new'),
            self.existing_excerpt_post_data,
            HTTP_HOST='thehost.example.com'
        )
        self.assertEqual(ExtractionOrder.objects.count(), 1)

        newly_created_order = ExtractionOrder.objects.first()  # only reproducible because there is only 1
        from osmaxx.excerptexport.models.extraction_order import ExtractionOrderState
        self.assertEqual(newly_created_order.state, ExtractionOrderState.INITIALIZED)
        self.assertIsNone(newly_created_order.process_start_date)
        self.assertIsNone(newly_created_order.process_reference)
        self.assertEqual(newly_created_order.orderer, self.user)
        self.assertEqual(newly_created_order.excerpt.name, 'Some old Excerpt')
