import subprocess
import os
from unittest.mock import MagicMock, patch

from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from excerptconverter.gisexcerptconverter import gis_excerpt_converter
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
    gis_excerpt_converter_export_formats = None
    converter_helper = None
    bbox_args = None

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
            'excerptconverter.gisexcerptconverter.gis_excerpt_converter': {
                'formats': ['gpkg', 'shp', 'spatialite'],
                'options': {
                }
            }
        }
        self.gis_excerpt_converter_export_formats = {
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
        self.extraction_order = models.ExtractionOrder.objects.create(
            orderer=self.user,
            excerpt=self.excerpt,
            extraction_configuration=self.extraction_configuration
        )
        self.result_file = self.result_storage.open(
            self.result_storage.save('abcd1234efgk5678.zip', ContentFile('Fancy gpkg file'))
        )
        self.converter_helper = ConverterHelper(self.extraction_order)
        bounding_geometry = self.extraction_order.excerpt.bounding_geometry
        self.bbox_args = ' '.join(str(coordinate) for coordinate in [
            bounding_geometry.west,
            bounding_geometry.south,
            bounding_geometry.east,
            bounding_geometry.north
        ])
        if not os.path.exists(private_storage.location):
            os.makedirs(private_storage.location)

    def tearDown(self):
        for result_file in self.result_storage.listdir('./')[1]:
            self.result_storage.delete(result_file)
        for storage_file in private_storage.listdir('./')[1]:
            private_storage.delete(storage_file)

    def test_create_output_file(self):
        original_storage_size = len(private_storage.listdir('./')[1])
        self.assertEqual(self.extraction_order.output_files.count(), 0)

        creation_status = gis_excerpt_converter.create_output_file(
            self.extraction_order,
            self.result_file.name,
            'gpkg'
        )
        output_file = self.extraction_order.output_files.get()

        self.assertTrue(creation_status)

        self.assertEqual(output_file.content_type, 'gpkg')
        self.assertEqual(output_file.file_extension, 'zip')
        self.assertEqual(output_file.mime_type, 'application/zip')
        self.assertEqual(private_storage.open(output_file.file).read(), b'Fancy gpkg file')

        self.assertEqual(len(private_storage.listdir('./')[1]), original_storage_size+1)
        self.assertTrue(private_storage.exists(output_file.file))
        self.assertFalse(self.result_storage.exists('abcd1234efgk5678.zip'))

    @patch('excerptconverter.gisexcerptconverter.gis_excerpt_converter')
    @patch.dict('excerptconverter.gisexcerptconverter.gis_excerpt_converter.EXPORT_FORMATS')
    @patch('subprocess.check_call')
    @patch('excerptconverter.converter_helper')
    @patch('os.listdir')
    def test_extract_excerpts(self, gis_excerpt_converter_mock, subprocess_check_call_mock,
                              excerptconverter_converter_helper_mock, os_listdir_mock):
        # return static value instead of implementation dependend
        # -> does not breaks tests on change of gis_excerpt_converter.EXPORT_FORMATS
        gis_excerpt_converter.EXPORT_FORMATS = self.gis_excerpt_converter_export_formats
        subprocess.check_call = MagicMock(return_value=0)
        # Do not create user messages
        self.converter_helper.inform_user = MagicMock()
        # Do not call the real method 'create_output_file'. This method is tested by an own test
        gis_excerpt_converter.create_output_file = MagicMock()
        # listdir should find one result file
        os.listdir = MagicMock(return_value=['some_file.txt'])

        gis_excerpt_converter.extract_excerpts(
            {'formats': ['gpkg', 'shp', 'some_not_existing']},
            self.extraction_order,
            self.bbox_args,
            self.converter_helper
        )

        call_command = "docker-compose run --rm excerpt python excerpt.py {bbox_args} -f {format_key}"

        subprocess.check_call.assert_any_call(
            call_command.format(bbox_args=self.bbox_args, format_key='gpkg').split(' ')
        )
        subprocess.check_call.assert_any_call(
            call_command.format(bbox_args=self.bbox_args, format_key='shp').split(' ')
        )
        self.assertEqual(subprocess.check_call.call_count, 2)
        self.assertEqual(gis_excerpt_converter.create_output_file.call_count, 2)

    @patch('excerptconverter.gisexcerptconverter.gis_excerpt_converter')
    @patch.dict('excerptconverter.gisexcerptconverter.gis_excerpt_converter.EXPORT_FORMATS')
    @patch('subprocess.check_output')
    @patch('subprocess.check_call')
    @patch('shutil.copyfile')
    @patch('excerptconverter.converter_helper')
    @patch('os.listdir')
    @patch('os.chdir')
    def test_execute_task(self, gis_excerpt_converter_mock, m2, m3, m4, m5, m6, m7):
        gis_excerpt_converter.EXPORT_FORMATS = self.gis_excerpt_converter_export_formats
        subprocess.check_output = MagicMock(return_value=0)
        subprocess.check_call = MagicMock(return_value=0)

        # Do not create user messages
        converter_helper = ConverterHelper(self.extraction_order)
        converter_helper.inform_user = MagicMock()
        converter_helper.file_conversion_finished = MagicMock()

        # Do not call the real methods. This methods are tested own tests
        gis_excerpt_converter_mock.extract_excerpts = MagicMock()

        os.listdir = MagicMock()
        os.chdir = MagicMock()

        gis_excerpt_converter.execute_task(
            self.extraction_order.id,
            self.gis_excerpt_converter_export_formats,
            self.extraction_configuration['excerptconverter.gisexcerptconverter.gis_excerpt_converter']
        )

        subprocess.check_output.assert_any_call("docker-compose pull".split(' '))
        subprocess.check_output.assert_any_call("docker-compose up -d db".split(' '))
        subprocess.check_call.assert_any_call((
            "docker-compose run --rm bootstrap sh main-bootstrap.sh {bbox_args}".format(bbox_args=self.bbox_args)
        ).split(' '))
        subprocess.check_call.assert_any_call("docker-compose stop --timeout 0".split(' '))
        subprocess.check_call.assert_any_call("docker-compose rm -v -f".split(' '))
