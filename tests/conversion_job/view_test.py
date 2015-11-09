from unittest.mock import patch

from django.test import TestCase

from conversion_job.models import Extent, ConversionJob, GISFormat
from conversion_job.views import ConversionJobStatusViewSet
from converters import converter_options
from shared import ConversionProgress
from rq.job import JobStatus as RQJobStatus


class Empty:
    pass


class DjangoRQGetQueueMock():
    def fetch_job(*args, **kwargs):
        rq_job_mock = Empty()
        rq_job_mock.status = RQJobStatus.STARTED
        rq_job_mock.meta = {'progress': ConversionProgress.STARTED}
        return rq_job_mock


def django_rq_get_queue_mock():
    django_rq_get_queue = DjangoRQGetQueueMock()
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

    @patch('django_rq.get_queue', django_rq_get_queue_mock)
    @patch('conversion_job.views.ConversionJobStatusViewSet.get_object', get_conversion_job)
    def test__update_status_from_rq(self, *args, **kwargs):
        conversion_job = get_conversion_job()

        self.assertEqual(
            min(conversion_job.gis_formats.values_list('progress', flat=True)),
            ConversionProgress.NEW.value
        )

        conversion_job_status_view = ConversionJobStatusViewSet(kwargs={'rq_job_id': self.conversion_job.rq_job_id})
        conversion_job_status_view._update_status_from_rq()

        self.assertEqual(
            min(conversion_job.gis_formats.values_list('progress', flat=True)),
            ConversionProgress.STARTED.value
        )
