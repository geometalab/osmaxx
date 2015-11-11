from unittest.mock import patch

from django.test import TestCase

from conversion_job.models import Extent, ConversionJob, GISFormat
from conversion_job.serializers import ConversionJobSerializer
from converters import converter_options


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
    def test_create(self, mock):
        self.assertEqual(GISFormat.objects.count(), 2)
        self.assertEqual(Extent.objects.count(), 1)
        self.assertEqual(ConversionJob.objects.count(), 1)
        data = {
            "gis_formats": converter_options.get_output_formats(),
            "callback_url": "http://example.com",
            "gis_option": {
                "crs": "WGS_84",
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
