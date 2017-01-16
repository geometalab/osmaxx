import os
import shutil
from unittest.mock import patch

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files import File
from django.contrib.auth.models import User
from django.conf import settings

from osmaxx.excerptexport.models import OutputFile, Excerpt, ExtractionOrder
from osmaxx.excerptexport.models import BBoxBoundingGeometry


@patch('osmaxx.job_progress.middleware.update_export')
class DownloadsTestCase(TestCase):
    def setUp(self):
        if not os.path.isdir(settings.PRIVATE_MEDIA_ROOT):
            os.makedirs(settings.PRIVATE_MEDIA_ROOT)

    def test_file_download(self, *args):
        user = User.objects.create_user('user', 'user@example.com', 'pw')
        bg = BBoxBoundingGeometry.create_from_bounding_box_coordinates(0, 0, 0, 0)
        excerpt = Excerpt.objects.create(name='Neverland', is_active=True, is_public=True, owner=user,
                                         bounding_geometry=bg)
        extraction_order = ExtractionOrder.objects.create(excerpt=excerpt, orderer=user)
        export = extraction_order.exports.create(file_format='fgdb')
        output_file = OutputFile.objects.create(mime_type='test/plain', export=export,
                                                file_extension='txt')

        file_path = os.path.join(settings.PRIVATE_MEDIA_ROOT, str(output_file.download_file_name))

        with open(file_path, 'w') as file_reference:
            new_file = File(file_reference)
            new_file.write('Test text')

        output_file.file = file_path
        output_file.save()

        response = self.client.get(
            reverse('excerptexport:download', kwargs={'uuid': output_file.public_identifier})
        )

        self.assertEqual(response['Content-Length'], str(os.path.getsize(file_path)))
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename=%s' % output_file.download_file_name
        )
        self.assertEqual(b''.join(response.streaming_content), b'Test text')

        os.remove(file_path)

    def tearDown(self):
        if os.path.isdir(settings.PRIVATE_MEDIA_ROOT):
            shutil.rmtree(settings.PRIVATE_MEDIA_ROOT)
