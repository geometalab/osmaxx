import os
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from conversion_job.models import Extent, ConversionJob, GISFormat
from converters import converter_settings, converter_options
from converters.boundaries import BBox
from shared import ConversionProgress
from tests.conversion_job.view_test import django_rq_get_queue_stub


class ExtentTest(TestCase):
    def test_clean_without_bbox_or_polyfile_raises_validation_error(self):
        e = Extent()
        self.assertRaisesRegex(ValidationError, r'either .* or .* must be given', e.clean)

    def test_clean_with_bbox_and_polyfile_raises_validation_error(self):
        e = Extent(west=0, south=0, east=0, north=0, polyfile='present')
        self.assertRaisesRegex(ValidationError, r'either .* or .* must be given', e.clean)

    def test_clean_with_incomplete_bbox_raises_validation_error(self):
        e = Extent(west=0, east=0)
        self.assertRaisesRegex(ValidationError, r'incomplete .* boundaries', e.clean)

    def test_clean_with_incomplete_bbox_and_polyfile_raises_validation_error(self):
        e = Extent(west=0, east=0, polyfile='present')
        self.assertRaisesRegex(ValidationError, r'either .* or .* must be given|incomplete .* boundaries', e.clean)

    def test_clean_with_bbox_only_passes(self):
        e = Extent(west=0, south=0, east=0, north=0)
        # no exception expected
        e.clean()

    def test_clean_with_polyfile_only_passes(self):
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

    def test_save_with_polyfile_succeeds(self):
        e = Extent(polyfile='present')
        # no exception expected
        e.save()

    def test_save_with_bbox_succeeds(self):
        e = Extent(west=0, south=0, east=0, north=0)
        # no exception expected
        e.save()


class ConversionJobTest(TestCase):
    def setUp(self):
        self.extent = Extent.objects.create(west=0, south=0, east=0, north=0)
        self.conversion_job = ConversionJob(extent=self.extent)
        self.conversion_job.save()

    def test_output_directory_if_not_exists_is_created(self):
        directory = self.conversion_job.output_directory
        os.rmdir(directory)
        self.assertFalse(os.path.exists(directory))
        directory = self.conversion_job.output_directory
        self.assertTrue(os.path.exists(directory))
        self.assertEqual(
            directory,
            os.path.join(converter_settings.OSMAXX_CONVERSION_SERVICE['RESULT_DIR'], str(self.conversion_job.id)))
        os.rmdir(directory)

    def test_get_resulting_file_path_or_none_with_format_when_no_file_is_available_returns_none(self):
        format = converter_options.get_output_formats()[0]
        self.assertIsNone(
            self.conversion_job.get_resulting_file_path_or_none(format=format)
        )

    def test_get_resulting_file_path_or_none_with_format_when_file_is_available_returns_file(self):
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

    def test_get_resulting_file_path_or_none_with_format_when_files_are_available_but_none_in_the_right_format_returns_none(self):
        # create a sample file with exception of the one for the unavailable_format
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

    def test_format_when_saved_returns_format(self):
        format_choice = converter_options.get_output_formats()[2]
        gis_format = GISFormat.objects.create(conversion_job=self.conversion_job, format=format_choice)
        self.assertEqual(
            self.conversion_job.get_conversion_options().get_output_formats()[0],
            gis_format.format
        )

    def test_progress_without_formats_returns_none(self):
        self.assertIsNone(self.conversion_job.progress)

    def test_progress_when_multiple_stati_are_set_returns_minimal_status_of_attached_gis_formats(self):
        GISFormat.objects.create(
            conversion_job=self.conversion_job,
            format=converter_options.get_output_formats()[1],
            progress=ConversionProgress.NEW.technical_representation
        )
        GISFormat.objects.create(
            conversion_job=self.conversion_job,
            format=converter_options.get_output_formats()[2],
            progress=ConversionProgress.STARTED.technical_representation
        )
        GISFormat.objects.create(
            conversion_job=self.conversion_job,
            format=converter_options.get_output_formats()[3],
            progress=ConversionProgress.SUCCESSFUL.technical_representation
        )
        self.assertIsNotNone(self.conversion_job.progress)
        self.assertEqual(
            self.conversion_job.progress,
            ConversionProgress.NEW.human_readable_name
        )

    @patch('django_rq.get_queue', django_rq_get_queue_stub)
    def test_update_status_from_rq_sets_the_value_to_started(self, *args, **kwargs):
        formats = converter_options.get_output_formats()
        for out_format in formats:
            GISFormat.objects.create(
                conversion_job=self.conversion_job,
                format=out_format
            )

        initial_progress_list = [ConversionProgress.NEW.technical_representation] * len(formats)
        model_progress_list = list(self.conversion_job.gis_formats.values_list('progress', flat=True))
        self.assertListEqual(model_progress_list, initial_progress_list)

        started_progress_list = [ConversionProgress.STARTED.technical_representation] * len(formats)
        self.conversion_job.update_status_from_rq()
        model_progress_list = list(self.conversion_job.gis_formats.values_list('progress', flat=True))
        self.assertListEqual(model_progress_list, started_progress_list)

        self.assertEqual(self.conversion_job.progress, ConversionProgress.STARTED.technical_representation)


class GISFormatTest(TestCase):
    def setUp(self):
        self.extent = Extent.objects.create(west=0, south=0, east=0, north=0)
        self.conversion_job = ConversionJob(extent=self.extent)
        self.conversion_job.save()

    def test_get_download_url_is_not_null(self):
        gis_format = GISFormat.objects.create(
            conversion_job=self.conversion_job,
            format=converter_options.get_output_formats()[1],
            progress=ConversionProgress.NEW.technical_representation
        )
        self.assertIsNotNone(gis_format.get_download_url(request=None))
