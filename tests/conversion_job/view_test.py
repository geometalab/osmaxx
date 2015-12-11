import os
from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from conversion_job.models import Extent, ConversionJob, GISFormat
from converters import converter_options
from shared import ConversionProgress
from rq.job import JobStatus as RQJobStatus


class Empty:
    pass


class DjangoRQGetQueueStub:
    def fetch_job(*args, **kwargs):
        rq_job_mock = Empty()
        rq_job_mock.status = RQJobStatus.STARTED
        rq_job_mock.meta = {'progress': ConversionProgress.STARTED}
        return rq_job_mock


def django_rq_get_queue_stub():
    django_rq_get_queue = DjangoRQGetQueueStub()
    return django_rq_get_queue


def get_conversion_job(*args, **kwargs):
    return ConversionJob.objects.first()


class ConversionJobStatusViewSetTest(TestCase):
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

    @patch('django_rq.get_queue', django_rq_get_queue_stub)
    @patch('conversion_job.views.ConversionJobStatusViewSet.get_object', get_conversion_job)
    def test_conversion_progress_when_created_is_new(self, *args, **kwargs):
        conversion_job = get_conversion_job()
        model_progress_list = list(conversion_job.gis_formats.values_list('progress', flat=True))
        self.assertListEqual(
            model_progress_list,
            [ConversionProgress.NEW.technical_representation] * len(model_progress_list)
        )
        self.assertEqual(conversion_job.progress, ConversionProgress.NEW.technical_representation)

    @patch('django_rq.get_queue', django_rq_get_queue_stub)
    @patch('conversion_job.views.ConversionJobStatusViewSet.get_object', get_conversion_job)
    def test_delete_result_when_file_available_removes_file_successfully(self):
        output_formats = self.conversion_job.get_conversion_options().get_output_formats()
        file_paths = [os.path.join(self.conversion_job.output_directory, '{0}.zip'.format(file_format))
                      for file_format in output_formats]
        try:
            for file_format_path in file_paths:
                open(file_format_path, 'x')
                self.assertTrue(os.path.exists(file_format_path) and os.path.isfile(file_format_path))

            url = reverse('gisformat-delete-result', kwargs=dict(pk=self.gis_format_1.id))
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            url = reverse('gisformat-delete-result', kwargs=dict(pk=self.gis_format_2.id))
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            for file_format_path in file_paths:
                self.assertFalse(os.path.exists(file_format_path))
        finally:
            for file_format_path in file_paths:
                try:
                    os.remove(file_format_path)
                except:
                    pass

    @patch('django_rq.get_queue', django_rq_get_queue_stub)
    @patch('conversion_job.views.ConversionJobStatusViewSet.get_object', get_conversion_job)
    def test_delete_result_when_file_unavailable_fails_silently(self):
        url = reverse('gisformat-delete-result', kwargs=dict(pk=self.gis_format_1.id))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('gisformat-delete-result', kwargs=dict(pk=self.gis_format_2.id))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
