import os
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from conversion_job.models import Extent, ConversionJob, GISFormat
from converters import converter_settings, converter_options
from converters.boundaries import BBox
from shared import ConversionProgress


class ExtentTest(TestCase):
    def test_validation_raised_in_clean(self):
        e = Extent()
        self.assertRaisesRegex(ValidationError, r'either .* or .* must be given', e.clean)

    def test_validation_raises_when_both_present(self):
        e = Extent(west=0, south=0, east=0, north=0, polyfile='present')
        self.assertRaisesRegex(ValidationError, r'either .* or .* must be given', e.clean)

    def test_validation_raises_with_incomplete_bbox(self):
        e = Extent(west=0, east=0)
        self.assertRaisesRegex(ValidationError, r'incomplete .* boundaries', e.clean)

    def test_validation_raises_with_polyfile_and_incomplete_bbox(self):
        e = Extent(west=0, east=0, polyfile='present')
        self.assertRaisesRegex(ValidationError, r'either .* or .* must be given|incomplete .* boundaries', e.clean)

    def test_validation_passes_with_bbox(self):
        e = Extent(west=0, south=0, east=0, north=0)
        # no exception expected
        e.clean()

    def test_validation_passes_with_polyfile(self):
        e = Extent(polyfile='present')
        # no exception expected
        e.clean()

    def test_get_geometry_returns_geometry(self):
        e = Extent(west=0, south=0, east=0, north=0)
        self.assertEqual(e.get_geometry().__dict__, BBox(west=0, south=0, east=0, north=0).__dict__)

    def test_get_geometry_raises_with_polyfile_for_now(self):
        e = Extent(polyfile='present')
        self.assertRaises(NotImplementedError, e.get_geometry)

    @patch('conversion_job.models.Extent.clean')
    def test_save_calls_clean_method(self, clean_mock):
        e = Extent(polyfile='present')
        e.save()
        clean_mock.assert_called_once_with()

    def test_save_call_succeeds_with_polyfile(self):
        e = Extent(polyfile='present')
        # no exception expected
        e.save()

    def test_save_call_succeeds_with_bbox(self):
        e = Extent(west=0, south=0, east=0, north=0)
        # no exception expected
        e.save()


class ConversionJobTest(TestCase):
    def setUp(self):
        self.extent = Extent.objects.create(west=0, south=0, east=0, north=0)
        self.conversion_job = ConversionJob(extent=self.extent)
        self.conversion_job.save()

    def test_output_directory_is_created_if_not_exists(self):
        directory = self.conversion_job.output_directory
        os.rmdir(directory)
        self.assertFalse(os.path.exists(directory))
        directory = self.conversion_job.output_directory
        self.assertTrue(os.path.exists(directory))
        self.assertEqual(
            directory,
            os.path.join(converter_settings.OSMAXX_CONVERSION_SERVICE['RESULT_DIR'], str(self.conversion_job.id)))
        os.rmdir(directory)

    def test_get_resulting_file_path_or_none_returns_none_with_unavailable_formats(self):
        format = converter_options.get_output_formats()[0]
        self.assertIsNone(
            self.conversion_job.get_resulting_file_path_or_none(format=format)
        )

    def test_get_resulting_file_path_or_none_returns_file_for_format(self):
        # create a sample file
        conversion_format = converter_options.get_output_formats()[0]
        filename = conversion_format + '.zip'
        out_dir = self.conversion_job.output_directory
        file_path = os.path.join(out_dir, filename)
        try:
            open(file_path, 'x').close()
            self.assertEqual(
                self.conversion_job.get_resulting_file_path_or_none(format=conversion_format),
                file_path
            )
        finally:
            # cleanup
            os.unlink(file_path)
            os.rmdir(out_dir)

    def test_get_resulting_file_path_or_none_returns_none_with_unavailable_format(self):
        # create a sample file
        conversion_format = converter_options.get_output_formats()[0]
        unavailable_format = converter_options.get_output_formats()[1]
        filename = conversion_format + '.zip'
        out_dir = self.conversion_job.output_directory
        file_path = os.path.join(out_dir, filename)
        try:
            open(file_path, 'x').close()
            self.assertIsNone(self.conversion_job.get_resulting_file_path_or_none(format=unavailable_format))
        finally:
            # cleanup
            os.unlink(file_path)
            os.rmdir(out_dir)

    def test_get_saved_conversions_options(self):
        format_choice = converter_options.get_output_formats()[2]
        gis_format = GISFormat.objects.create(conversion_job=self.conversion_job, format=format_choice)
        self.assertEqual(
            self.conversion_job.get_conversion_options().get_output_formats()[0],
            gis_format.format
        )

    def test_progress_returns_none_without_formats(self):
        self.assertIsNone(self.conversion_job.progress)

    def test_progress_returns_minimal_status_of_attached_gis_formats(self):
        GISFormat.objects.create(
            conversion_job=self.conversion_job,
            format=converter_options.get_output_formats()[1],
            progress=ConversionProgress.NEW.value
        )
        GISFormat.objects.create(
            conversion_job=self.conversion_job,
            format=converter_options.get_output_formats()[2],
            progress=ConversionProgress.STARTED.value
        )
        GISFormat.objects.create(
            conversion_job=self.conversion_job,
            format=converter_options.get_output_formats()[3],
            progress=ConversionProgress.SUCCESSFUL.value
        )
        self.assertIsNotNone(self.conversion_job.progress)
        self.assertEqual(
            self.conversion_job.progress,
            [tup[1] for tup in ConversionProgress.choices() if tup[0] == ConversionProgress.NEW.value][0]
        )


class GISFormatTest(TestCase):
    def setUp(self):
        self.extent = Extent.objects.create(west=0, south=0, east=0, north=0)
        self.conversion_job = ConversionJob(extent=self.extent)
        self.conversion_job.save()

    def test_get_download_url(self):
        gis_format = GISFormat.objects.create(
            conversion_job=self.conversion_job,
            format=converter_options.get_output_formats()[1],
            progress=ConversionProgress.NEW.value
        )
        self.assertIsNotNone(gis_format.get_download_url(request=None))
