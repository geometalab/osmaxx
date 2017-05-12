from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.contrib.gis import geos
from hamcrest import assert_that, contains_inanyorder as contains_in_any_order

from osmaxx.conversion import output_format, status
from osmaxx.excerptexport import models


class ExtractionOrderTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'pw')

        self.excerpt = models.Excerpt.objects.create(
            name='Neverland',
            is_active=True,
            is_public=False,
            owner=self.user,
            # FIXME: use the bounding_geometry fixture for this
            bounding_geometry=geos.GEOSGeometry(
                '{"type":"MultiPolygon","coordinates":[[[[8.815935552120209,47.222220486817676],[8.815935552120209,47.22402752311505],[8.818982541561127,47.22402752311505],[8.818982541561127,47.222220486817676],[8.815935552120209,47.222220486817676]]]]}'
            )
        )
        self.coordinate_reference_system = 4326

    def test_create_extraction_order_with_extraction_configuration_and_retrieve_extraction_configuration(self):
        extraction_order_id = models.ExtractionOrder.objects.create(
            excerpt=self.excerpt,
            orderer=self.user,
            coordinate_reference_system=self.coordinate_reference_system,
            extraction_formats=['txt'],
        ).id
        extraction_order = models.ExtractionOrder.objects.get(pk=extraction_order_id)
        assert_that(extraction_order.extraction_formats, contains_in_any_order('txt'))
        assert extraction_order.coordinate_reference_system == 4326

    def test_create_and_retrieve_extraction_configuration_on_exising_extraction_configuration(self):
        extraction_order = models.ExtractionOrder.objects.create(
            excerpt=self.excerpt,
            orderer=self.user,
        )
        extraction_order.coordinate_reference_system = self.coordinate_reference_system
        extraction_order.extraction_formats = ['txt']
        assert_that(extraction_order.extraction_formats, contains_in_any_order('txt'))
        assert extraction_order.coordinate_reference_system == 4326

    def test_retrieve_extraction_configuration_on_saved_extraction_configuration(self):
        extraction_order = models.ExtractionOrder.objects.create(
            excerpt=self.excerpt,
            orderer=self.user,
        )
        extraction_order.coordinate_reference_system = self.coordinate_reference_system
        extraction_order.extraction_formats = ['txt']
        extraction_order.save()
        extraction_order_id = extraction_order.id
        extraction_order = models.ExtractionOrder.objects.get(pk=extraction_order_id)
        assert_that(extraction_order.extraction_formats, contains_in_any_order('txt'))
        assert extraction_order.coordinate_reference_system == 4326


def test_export_get_export_status_changed_message_does_not_html_escape_format_description():
    excerpt = models.Excerpt(name='Obersee')
    extraction_order = models.ExtractionOrder(excerpt=excerpt)
    export = models.Export(id=5, status=status.FINISHED, extraction_order=extraction_order, file_format=output_format.GARMIN)
    assert export._get_export_status_changed_message() == \
        'Export #5 "Obersee" to Garmin navigation & map data has finished.'
