import collections
import datetime

from django.utils import timezone
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from excerptconverter import ConverterManager, converter_registry
from excerptconverter.gisexcerptconverter import gis_excerpt_converter
from . import some_excerpt_converter, just_for_test_excerpt_converter, test_result_pipe

from osmaxx.excerptexport import models


class ConverterManagerTestCase(TestCase):
    user = None
    excerpt = None
    extraction_order = None
    extraction_configuration = None

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'pw')
        self.excerpt = models.Excerpt.objects.create(
            name='Neverland',
            is_active=True,
            is_public=False,
            owner=self.user,
            bounding_geometry=models.OsmosisPolygonFilterBoundingGeometry.objects.create(
                polygon_file=SimpleUploadedFile('in_memory_file.poly', b'the file content (not a real .poly file)')
            )
        )
        self.extraction_configuration = {
            'excerptconverter.tests.just_for_test_excerpt_converter': {
                'formats': ['jpg', 'svg'],
                'options': {
                    'quality': 8
                }
            }
        }
        self.extraction_order = models.ExtractionOrder.objects.create(
            orderer=self.user,
            excerpt=self.excerpt,
            extraction_configuration=self.extraction_configuration
        )
        test_result_pipe.temp_result_storage = None

        if just_for_test_excerpt_converter not in converter_registry.available_converters:
            converter_registry.available_converters.append(just_for_test_excerpt_converter)
        if some_excerpt_converter not in converter_registry.available_converters:
            converter_registry.available_converters.append(some_excerpt_converter)

    def tearDown(self):
        test_result_pipe.temp_result_storage = None

        if just_for_test_excerpt_converter in converter_registry.available_converters:
            converter_registry.available_converters.remove(just_for_test_excerpt_converter)
        if some_excerpt_converter in converter_registry.available_converters:
            converter_registry.available_converters.remove(some_excerpt_converter)

    def test_converter_configuration(self):
        self.assertEqual(
            # Usage of ordered dict because dict is not sorted, so we will get an arbitrary order -> not testable
            collections.OrderedDict(sorted(ConverterManager.converter_configuration().items())),
            collections.OrderedDict(sorted({
                some_excerpt_converter.__name__: some_excerpt_converter.converter_configuration(),
                just_for_test_excerpt_converter.__name__: just_for_test_excerpt_converter.converter_configuration(),
                gis_excerpt_converter.__name__: gis_excerpt_converter.converter_configuration()
            }.items()))
        )

    def test_full_converter_pipeline(self):
        converter_manager = ConverterManager(self.extraction_order, run_as_celery_tasks=False)
        converter_manager.execute_converters()
        self.assertTrue(converter_manager.extraction_order.process_start_date < timezone.now())
        self.assertTrue(
            converter_manager.extraction_order.process_start_date > (timezone.now()-datetime.timedelta(0, 1))
        )
        self.assertEqual(
            collections.OrderedDict(sorted(test_result_pipe.temp_result_storage.items())),
            collections.OrderedDict(sorted({
                'excerpt_name': 'Neverland',
                'supported_formats': sorted(['JPG', 'PNG', 'SVG']),
                'conversion_formats': ['jpg', 'svg'],
                'conversion_options_quality': 8
            }.items()))
        )
        self.assertEqual(
            models.ExtractionOrder.objects.get(pk=self.extraction_order.id).state,
            models.ExtractionOrderState.FINISHED
        )
