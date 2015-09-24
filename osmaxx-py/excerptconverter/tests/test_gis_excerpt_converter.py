import subprocess
import os
from unittest.mock import MagicMock, patch

from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from excerptconverter.gisexcerptconverter import GisExcerptConverter
from excerptconverter import ConverterHelper

from osmaxx.excerptexport import models

from osmaxx.utils import private_storage


class GisExcerptConverterTestCase(TestCase):
    # tests:
    # start process correct
    # handle return correct

    user = None
    excerpt = None
    extraction_order = None
    result_storage = FileSystemStorage(location=settings.RESULT_MEDIA_ROOT)
    result_file = None
    extraction_configuration = None
    gis_excerpt_converter_export_formats = {
        'spatialite': {
            'name': 'SpatiaLite (SQLite)',
            'file_extension': 'sqlite'
        },
        'gpkg': {
            'name': 'Geo package',
            'file_extension': 'gpkg'
        },
        'shp': {
            'name': 'Shape file',
            'file_extension': 'shp'
        }
    }

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'pw')

        bounding_geometry = models.BBoxBoundingGeometry.create_from_bounding_box_coordinates(
            48.1234, 9.5678, 46.9012, 6.3456
        )
        bounding_geometry.save()

        self.excerpt = models.Excerpt.objects.create(
            name='Neverland',
            is_active=True,
            is_public=True,
            owner=self.user,
            bounding_geometry=bounding_geometry
        )
        self.extraction_configuration = {
            'GisExcerptConverter': {
                'formats': ['gpkg', 'shp', 'spatialite'],
                'options': {
                }
            }
        }
        self.extraction_order = models.ExtractionOrder.objects.create(
            orderer=self.user,
            excerpt=self.excerpt,
            extraction_configuration=self.extraction_configuration
        )
        self.result_file = self.result_storage.open(
            self.result_storage.save('abcd1234efgk5678.zip', ContentFile('Fancy gpkg file'))
        )

    def tearDown(self):
        for result_file in self.result_storage.listdir('./')[1]:
            self.result_storage.delete(result_file)
        for storage_file in private_storage.listdir('./')[1]:
            private_storage.delete(storage_file)

    def test_create_output_file(self):
        original_storage_size = len(private_storage.listdir('./')[1])
        self.assertEqual(self.extraction_order.output_files.count(), 0)

        creation_status = GisExcerptConverter.create_output_file(self.extraction_order, self.result_file.name, 'gpkg')
        output_file = self.extraction_order.output_files.get()

        self.assertTrue(creation_status)

        self.assertEqual(output_file.content_type, 'gpkg')
        self.assertEqual(output_file.file_extension, 'zip')
        self.assertEqual(output_file.mime_type, 'application/zip')
        self.assertEqual(private_storage.open(output_file.file).read(), b'Fancy gpkg file')

        self.assertEqual(len(private_storage.listdir('./')[1]), original_storage_size+1)
        self.assertTrue(private_storage.exists(output_file.file))
        self.assertFalse(self.result_storage.exists('abcd1234efgk5678.zip'))

    @patch('excerptconverter.gisexcerptconverter.GisExcerptConverter')
    @patch('subprocess.check_call')
    @patch('excerptconverter.converter_helper')
    @patch('os.listdir')
    def test_extract_excerpts(self, GisExcerptConverter_mock, subprocess_check_call_mock,
                              excerptconverter_converter_helper_mock, os_listdir_mock):
        converter_helper = ConverterHelper(self.extraction_order)
        bounding_geometry = self.extraction_order.excerpt.bounding_geometry
        bbox_args = ' '.join(str(coordinate) for coordinate in [
            bounding_geometry.west,
            bounding_geometry.south,
            bounding_geometry.east,
            bounding_geometry.north
        ])

        # return static value instead of implementation dependend
        # -> does not breaks tests on change of GisExcerptConverter.export_formats
        GisExcerptConverter.export_formats = MagicMock(return_value=self.gis_excerpt_converter_export_formats)
        subprocess.check_call = MagicMock(return_value=0)
        # Do not create user messages
        converter_helper.inform_user = MagicMock()
        # Do not call the real method 'create_output_file'. This method is tested by an own test
        GisExcerptConverter.create_output_file = MagicMock()
        # listdir should find one result file
        os.listdir = MagicMock(return_value=['some_file.txt'])

        GisExcerptConverter.extract_excerpts(
            {'formats': ['gpkg', 'shp', 'some_not_existing']},
            self.extraction_order,
            bbox_args,
            converter_helper
        )

        call_command = "docker-compose run --rm excerpt python excerpt.py {bbox_args} -f {format_key}"

        subprocess.check_call.assert_any_call(call_command.format(bbox_args=bbox_args, format_key='gpkg').split(' '))
        subprocess.check_call.assert_any_call(call_command.format(bbox_args=bbox_args, format_key='shp').split(' '))
        self.assertEqual(subprocess.check_call.call_count, 2)
        self.assertEqual(GisExcerptConverter.create_output_file.call_count, 2)
