import collections
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from excerptconverter import ConverterManager
from excerptconverter.baseexcerptconverter import BaseExcerptConverter
from excerptconverter.dummyexcerptconverter import DummyExcerptConverter

from osmaxx.excerptexport import models


class SomeExcerptConverter(BaseExcerptConverter):
    @staticmethod
    def name():
        return 'Dummy'

    @staticmethod
    def export_formats():
        return {
            'jpg': {
                'name': 'JPG',
                'file_extension': 'jpg',
                'mime_type': 'image/jpg'
            }
        }

    @staticmethod
    def export_options():
        return {
            'resolution': {
                'label': 'Resolution',
                'type': 'text',
                'default': '200'
            }
        }


class TestExcerptConverter(BaseExcerptConverter):
    @staticmethod
    def name():
        return 'Test'

    @staticmethod
    def export_formats():
        return {
            'jpg': {
                'name': 'JPG',
                'file_extension': 'jpg',
                'mime_type': 'image/jpg'
            },
            'png': {
                'name': 'PNG',
                'file_extension': 'png',
                'mime_type': 'image/png'
            },
            'svg': {
                'name': 'SVG',
                'file_extension': 'svg',
                'mime_type': 'image/svg'
            }
        }

    @staticmethod
    def export_options():
        return {
            'image_resolution': {
                'label': 'Resolution',
                'type': 'number',
                'default': '500'
            },
            'quality': {
                'label': 'Quality',
                'type': 'number',
                'default': '10'
            }
        }

    @staticmethod
    def execute_task(extraction_order_id, supported_export_formats, converter_configuration):
        extraction_order = models.ExtractionOrder.objects.get(pk=extraction_order_id)
        ConverterManagerTestCase.temp_result_storage = {
            'excerpt_name': extraction_order.excerpt.name,
            'supported_formats': sorted([export_format_configuration['name']
                                        for export_format_configuration
                                        in supported_export_formats.values()]),
            'conversion_formats': converter_configuration['formats'],
            'conversion_options_quality': converter_configuration['options']['quality']
        }
        extraction_order.state = models.ExtractionOrderState.FINISHED
        extraction_order.save()


class ConverterManagerTestCase(TestCase):
    temp_result_storage = None
    user = None
    excerpt = None
    extraction_order = None
    extraction_configuration = None

    def setUp(self):
        if SomeExcerptConverter not in BaseExcerptConverter.available_converters:
            BaseExcerptConverter.available_converters.append(SomeExcerptConverter)
            BaseExcerptConverter.available_converters.append(TestExcerptConverter)

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
            'TestExcerptConverter': {
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
        self.temp_result_storage = None

    def tearDown(self):
        if SomeExcerptConverter in BaseExcerptConverter.available_converters:
            BaseExcerptConverter.available_converters.remove(SomeExcerptConverter)
            BaseExcerptConverter.available_converters.remove(TestExcerptConverter)
        self.temp_result_storage = None

    def test_converter_configuration(self):
        self.assertEqual(
            # Usage of ordered dict because dict is not sorted, so we will get an arbitrary order -> not testable
            collections.OrderedDict(sorted(ConverterManager.converter_configuration().items())),
            collections.OrderedDict(sorted({
                SomeExcerptConverter.__name__: SomeExcerptConverter.converter_configuration(),
                DummyExcerptConverter.__name__: DummyExcerptConverter.converter_configuration(),
                TestExcerptConverter.__name__: TestExcerptConverter.converter_configuration()
            }.items()))
        )

    def test_full_converter_pipeline(self):
        converter_manager = ConverterManager(self.extraction_order, run_as_celery_tasks=False)
        converter_manager.execute_converters()
        self.assertEqual(
            collections.OrderedDict(sorted(ConverterManagerTestCase.temp_result_storage.items())),
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
