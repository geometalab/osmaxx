from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from excerptconverter.gisexcerptconverter import GisExcerptConverter

from osmaxx.excerptexport import models

from osmaxx.utils import private_storage


class GisExcerptConverterTestCase(TestCase):
    # tests:
    # start process correct
    # handle return correct
    # copy result file correct

    user = None
    excerpt = None
    extraction_order = None
    result_storage = FileSystemStorage(location=settings.RESULT_MEDIA_ROOT)
    result_file = None

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
        extraction_configuration = {
            'TestExcerptConverter': {
                'formats': ['gpkg', 'shp'],
                'options': {
                }
            }
        }
        self.extraction_order = models.ExtractionOrder.objects.create(
            orderer=self.user,
            excerpt=self.excerpt,
            extraction_configuration=extraction_configuration
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
