from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from hamcrest import assert_that, contains_inanyorder as contains_in_any_order

from osmaxx.conversion.converters.converter_gis.detail_levels import DETAIL_LEVEL_ALL
from osmaxx.excerptexport.models import ExtractionOrder, Excerpt
from tests.excerptexport.permission_test_helper import PermissionHelperMixin
from tests.test_helpers import vcr_explicit_path as vcr


class ExcerptExportViewTests(TestCase, PermissionHelperMixin):
    def setUp(self):
        from django.contrib.gis import geos
        # FIXME: use the bounding_geometry fixture for this
        multi_polygon = geos.GEOSGeometry('{"type":"MultiPolygon","coordinates":[[[[8.815935552120209,47.222220486817676],[8.815935552120209,47.22402752311505],[8.818982541561127,47.22402752311505],[8.818982541561127,47.222220486817676],[8.815935552120209,47.222220486817676]]]]}')
        self.user = User.objects.create_user('user', 'user@example.com', 'pw')
        other_user = User.objects.create_user('other_user', 'o_u@example.com', 'o_pw')

        self.coordinate_reference_system = 4326
        self.detail_level = DETAIL_LEVEL_ALL

        self.new_excerpt_post_data = {
            'name': 'A very interesting region',
            'bounding_geometry': '{"type":"Polygon","coordinates":[[[8.815935552120209,47.222220486817676],[8.815935552120209,47.22402752311505],[8.818982541561127,47.22402752311505],[8.818982541561127,47.222220486817676],[8.815935552120209,47.222220486817676]]]}',
            'formats': ['fgdb'],
            'coordinate_reference_system': self.coordinate_reference_system,
            'detail_level': self.detail_level,
        }
        self.existing_own_excerpt = Excerpt.objects.create(
            name='Some old Excerpt',
            is_active=True,
            is_public=False,
            owner=self.user,
            bounding_geometry=multi_polygon
        )
        self.existing_public_foreign_excerpt = Excerpt.objects.create(
            name='Public Excerpt by someone else',
            is_active=True,
            is_public=True,
            owner=other_user,
            bounding_geometry=multi_polygon
        )
        self.existing_private_foreign_excerpt = Excerpt.objects.create(
            name='Private Excerpt by someone else',
            is_active=True,
            is_public=False,
            owner=other_user,
            bounding_geometry=multi_polygon
        )
        self.existing_excerpt_post_data = {
            'existing_excerpts': self.existing_own_excerpt.id,
            'formats': ['fgdb'],
            'coordinate_reference_system': self.coordinate_reference_system,
            'detail_level': self.detail_level,
        }

    def test_new_when_not_logged_in(self):
        """
        When not logged in, we get redirected.
        """
        response = self.client.get(reverse('excerptexport:order_new_excerpt'))
        self.assertEqual(response.status_code, 302)

    @vcr.use_cassette('fixtures/vcr/views-test_test_new.yml')
    def test_new(self):
        """
        When logged in, we get the excerpt choice form.
        """
        self.add_valid_email()
        self.client.login(username='user', password='pw')
        response = self.client.get(reverse('excerptexport:order_new_excerpt'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order New Excerpt')

    @vcr.use_cassette('fixtures/vcr/views-test_test_new_offers_existing_own_excerpt.yml')
    def test_new_offers_existing_own_excerpt(self):
        self.add_valid_email()
        self.client.login(username='user', password='pw')
        response = self.client.get(reverse('excerptexport:order_existing_excerpt'))
        self.assertIn(
            ('Personal excerpts (user) [1]', ((self.existing_own_excerpt.id, 'Some old Excerpt'),)),
            response.context['form'].fields['existing_excerpts'].choices
        )
        self.assertIn(self.existing_own_excerpt.name, response.context['form'].form_html)

    @vcr.use_cassette('fixtures/vcr/views-test_test_new_offers_existing_public_foreign_excerpt.yml')
    def test_new_offers_existing_public_foreign_excerpt(self):
        self.add_valid_email()
        self.client.login(username='user', password='pw')
        response = self.client.get(reverse('excerptexport:order_existing_excerpt'))

        self.assertIn(
            ('Public excerpts [1]', ((self.existing_public_foreign_excerpt.id, 'Public Excerpt by someone else'),)),
            response.context['form'].fields['existing_excerpts'].choices
        )
        self.assertIn(self.existing_public_foreign_excerpt.name, response.context['form'].form_html)

    @vcr.use_cassette('fixtures/vcr/views-test_new_doesnt_offer_existing_private_foreign_excerpt.yml')
    def test_new_doesnt_offer_existing_private_foreign_excerpt(self):
        self.add_valid_email()
        self.client.login(username='user', password='pw')
        response = self.client.get(reverse('excerptexport:order_existing_excerpt'))
        self.assertNotContains(response, self.existing_private_foreign_excerpt.name)

    def test_create_when_not_logged_in(self):
        """
        When not logged in, we get redirected.
        """
        response = self.client.post(reverse('excerptexport:order_new_excerpt'), self.new_excerpt_post_data)
        self.assertEqual(response.status_code, 302)

    @vcr.use_cassette('fixtures/vcr/views-test_create_with_new_excerpt.yml')
    def test_create_with_new_excerpt(self):
        """
        When logged in, POSTing an export request with a new excerpt is successful.
        """
        self.add_valid_email()
        self.client.login(username='user', password='pw')
        response = self.client.post(
            reverse('excerptexport:order_new_excerpt'),
            self.new_excerpt_post_data,
            HTTP_HOST='thehost.example.com'
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Excerpt.objects.filter(name='A very interesting region', is_active=True, is_public=False).count(),
            1
        )

    @vcr.use_cassette('fixtures/vcr/views-test_create_with_new_excerpt.yml')
    def test_create_with_new_excerpt_ignores_ispublic(self):
        """
        When logged in, POSTing an export request with a new excerpt is successful.
        """
        self.add_valid_email()
        self.client.login(username='user', password='pw')
        self.new_excerpt_post_data['is_public'] = True
        response = self.client.post(
            reverse('excerptexport:order_new_excerpt'),
            self.new_excerpt_post_data,
            HTTP_HOST='thehost.example.com'
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Excerpt.objects.filter(name='A very interesting region', is_active=True, is_public=False).count(),
            1
        )
        self.assertEqual(
            Excerpt.objects.filter(name='A very interesting region', is_public=True).count(),
            0
        )

    @vcr.use_cassette('fixtures/vcr/views-test_create_with_existing_excerpt.yml')
    def test_create_with_existing_excerpt(self):
        """
        When logged in, POSTing an export request using an existing excerpt is successful.
        """
        self.add_valid_email()
        self.client.login(username='user', password='pw')
        response = self.client.post(
            reverse('excerptexport:order_existing_excerpt'),
            self.existing_excerpt_post_data,
            HTTP_HOST='thehost.example.com'
        )
        self.assertEqual(response.status_code, 302)  # this should be a redirect when successful
        self.assertEqual(ExtractionOrder.objects.filter(
            excerpt_id=self.existing_excerpt_post_data['existing_excerpts']
        ).count(), 1)  # only reproducible because there is only 1

    @vcr.use_cassette('fixtures/vcr/views-test_create_with_new_excerpt_persists_a_new_order.yml')
    def test_create_with_new_excerpt_persists_a_new_order(self):
        """
        When logged in, POSTing an export request with a new excerpt persists a new ExtractionOrder.
        """
        self.add_valid_email()
        self.assertEqual(ExtractionOrder.objects.count(), 0)
        self.client.login(username='user', password='pw')
        self.client.post(reverse('excerptexport:order_new_excerpt'),
                         self.new_excerpt_post_data, HTTP_HOST='thehost.example.com')
        self.assertEqual(ExtractionOrder.objects.count(), 1)

        newly_created_order = ExtractionOrder.objects.first()  # only reproducible because there is only 1
        self.assertEqual(newly_created_order.coordinate_reference_system, self.coordinate_reference_system)
        self.assertEqual(newly_created_order.detail_level, self.detail_level)
        assert_that(newly_created_order.extraction_formats, contains_in_any_order('fgdb'))
        self.assertEqual(newly_created_order.orderer, self.user)
        self.assertEqual(newly_created_order.excerpt.name, 'A very interesting region')

    @vcr.use_cassette('fixtures/vcr/views-test_create_with_existing_excerpt_persists_a_new_order.yml')
    def test_create_with_existing_excerpt_persists_a_new_order(self):
        """
        When logged in, POSTing an export request using an existing excerpt persists a new ExtractionOrder.
        """
        self.add_valid_email()
        self.assertEqual(ExtractionOrder.objects.count(), 0)
        self.client.login(username='user', password='pw')
        self.client.post(
            reverse('excerptexport:order_existing_excerpt'),
            self.existing_excerpt_post_data,
            HTTP_HOST='thehost.example.com'
        )
        self.assertEqual(ExtractionOrder.objects.count(), 1)

        newly_created_order = ExtractionOrder.objects.first()  # only reproducible because there is only 1
        self.assertEqual(newly_created_order.coordinate_reference_system, self.coordinate_reference_system)
        self.assertEqual(newly_created_order.detail_level, self.detail_level)
        assert_that(newly_created_order.extraction_formats, contains_in_any_order('fgdb'))
        self.assertEqual(newly_created_order.orderer, self.user)
        self.assertEqual(newly_created_order.excerpt.name, 'Some old Excerpt')
