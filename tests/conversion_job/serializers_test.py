import os
import shutil
from unittest.mock import patch, ANY

from collections import namedtuple
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase

from conversion_job.models import Extent, ConversionJob, GISFormat
from conversion_job.serializers import ConversionJobSerializer, GISFormatStatusSerializer
from converters import converter_options
from django.test.utils import override_settings
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from shared import ConversionProgress


class RQJobMock:
    id = ''.join(['1' for _ in range(36)])


class GISFormatListSerializerTest(TestCase):
    def setUp(self):
        self.extent = Extent.objects.create(west=0, south=0, east=0, north=0)
        self.conversion_job = ConversionJob.objects.create(extent=self.extent)
        self.gis_format_1 = GISFormat.objects.create(
            conversion_job=self.conversion_job,
            format=converter_options.get_output_formats()[0]
        )
        self.gis_format_2 = GISFormat.objects.create(
            conversion_job=self.conversion_job,
            format=converter_options.get_output_formats()[3]
        )

    @patch('conversion_job.serializers.ConversionJobSerializer._enqueue_rq_job', return_value=RQJobMock)
    def test_create_succeeds(self, mock):
        self.assertEqual(GISFormat.objects.count(), 2)
        self.assertEqual(Extent.objects.count(), 1)
        self.assertEqual(ConversionJob.objects.count(), 1)
        data = {
            "gis_formats": converter_options.get_output_formats(),
            "callback_url": "http://example.com",
            "gis_options": {
                "coordinate_reference_system": "WGS_84",
                "detail_level": 1,
            },
            "extent": {
                "west": 29.525547623634335,
                "south": 40.77546776498174,
                "east": 29.528980851173397,
                "north": 40.77739734768811,
                "polyfile": None,
            }
        }
        conversion_job_serializer = ConversionJobSerializer(data=data)
        conversion_job_serializer.is_valid()
        conversion_job_serializer.save()

        self.assertEqual(Extent.objects.count(), 2)
        self.assertEqual(GISFormat.objects.count(), 2 + len(converter_options.get_output_formats()))
        self.assertEqual(ConversionJob.objects.count(), 2)

        args, kwargs = mock.call_args
        self.assertCountEqual(kwargs['format_options'].output_formats, converter_options.get_output_formats())

        self.assertNotEqual(self.conversion_job, ConversionJob.objects.last())


class GISFormatStatusSerializerTest(TestCase):
    def setUp(self):
        extent = Extent.objects.create(west=0, south=0, east=0, north=0)
        self.conversion_job = ConversionJob.objects.create(extent=extent)
        self.gis_format = GISFormat.objects.create(
            conversion_job=self.conversion_job,
            format=converter_options.get_output_formats()[0]
        )
        request = HttpRequest()
        request.META['HTTP_HOST'] = 'some-host'
        self.format_status_serializer = GISFormatStatusSerializer(self.gis_format, context={'request': request})

    def tearDown(self):
        shutil.rmtree(self.conversion_job.output_directory)
        super().tearDown()

    def _create_valid_files(self):
        matching_file_names = ['{}.zip'.format(f) for f in converter_options.get_output_formats()]
        for matching_file_name in matching_file_names:
            open(os.path.join(self.conversion_job.output_directory, matching_file_name), 'x').close()

    def test_get_download_url_when_file_is_not_available_is_none(self):
        self.gis_format.progress = ConversionProgress.SUCCESSFUL.technical_representation
        self.gis_format.save()
        self.assertIsNone(self.format_status_serializer.data.get('result_url'))

    def test_get_download_url_when_status_is_success_and_file_available_is_defined(self):
        self._create_valid_files()
        self.gis_format.progress = ConversionProgress.SUCCESSFUL.technical_representation
        self.gis_format.save()
        self.assertIsNotNone(self.format_status_serializer.data.get('result_url'))

    def test_get_download_url_when_status_raises_error_when_deleted_is_defined(self):
        self.gis_format.delete()
        with self.assertRaises(GISFormat.DoesNotExist):
            # self.format_status_serializer.data already raises, but .get does raise as well.
            self.format_status_serializer.data.get('result_url')


class HostTest(APITestCase):

    test_host = 'the-host.example.com'

    rq_job_stub = namedtuple('RQJob', ['id'])(id='0' * 36)

    @override_settings(ALLOWED_HOSTS=[test_host])
    @patch('manager.job_manager.ConversionJobManager.start_conversion', return_value=rq_job_stub)
    def test_foo(self, start_conversion_mock):
        data = {
            "callback_url": "http://callback.example.com",
            "gis_formats": [
                "fgdb"
            ],
            "gis_options": {
                "coordinate_reference_system": "WGS_84",
                "detail_level": 1
            },
            "extent": {
                "west": 7.38777995109558,
                "south": 47.1948706159031,
                "east": 7.39292979240417,
                "north": 47.1972544966946,
                "polyfile": None
            }
        }
        user = User.objects.create_user(username='lauren', password='lauri', email=None)
        self.client.force_authenticate(user=user)
        self.client.post(reverse('conversionjob-list'), data, format='json', HTTP_HOST=self.test_host)
        expected_host = self.test_host
        start_conversion_mock.assert_called_with(ANY, ANY, expected_host)
