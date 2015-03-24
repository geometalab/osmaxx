import os

from django.test import TestCase

from django.core.urlresolvers import reverse
from django.core.files import File

from django.contrib.auth.models import User

from excerptexport.models import OutputFile, Excerpt, ExtractionOrder
from excerptexport import settings


class DownloadsTestCase(TestCase):
    def setUp(self):
        settings.APPLICATION_SETTINGS['data_directory'] = '/tmp/osmaxx-dev-data'
        if not os.path.isdir(settings.APPLICATION_SETTINGS['data_directory']):
            os.makedirs(settings.APPLICATION_SETTINGS['data_directory'])
        settings.APPLICATION_SETTINGS['download_file_name'] = '%(name)s'

    def test_file_download(self):
        user = User.objects.create_user('user', 'user@example.com', 'pw')
        excerpt = Excerpt.objects.create(name='Neverland', is_active=True, is_public=True, owner=user)
        extraction_order = ExtractionOrder.objects.create(excerpt=excerpt, orderer=user)
        output_file = OutputFile.objects.create(mime_type='test/plain', extraction_order=extraction_order)

        file_path = settings.APPLICATION_SETTINGS['data_directory'] + '/' + output_file.public_identifier + '.txt'

        with open(file_path, 'w') as file_reference:
            new_file = File(file_reference)
            new_file.write('Test text')

        # file must be committed, so reopen to attach to model
        output_file.file = file_path
        output_file.save()


        response = self.client.get(
            reverse('excerptexport:download'),
            {'file': output_file.public_identifier}
        )
        
        self.assertEqual(response['Content-Length'], str(os.path.getsize(file_path)))
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename=%s' % os.path.basename(output_file.file.name)
        )
        self.assertEqual(b''.join(response.streaming_content), b'Test text')

        os.remove(file_path)
