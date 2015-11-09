from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from conversion_job.models import Extent, ConversionJob
from converters.boundaries import BBox


class ExtentTest(TestCase):
    def test_validation_raised_in_clean(self):
        e = Extent()
        self.assertFalse(e._bbox_present())
        self.assertFalse(e._polyfile_present())
        self.assertRaisesRegex(ValidationError, r'either .* or .* must be given', e.clean)

    def test_validation_raises_when_both_present(self):
        e = Extent(west=0, south=0, east=0, north=0, polyfile='present')
        self.assertTrue(e._bbox_present())
        self.assertTrue(e._polyfile_present())
        self.assertRaisesRegex(ValidationError, r'either .* or .* must be given', e.clean)

    def test_validation_raises_with_incomplete_bbox(self):
        e = Extent(west=0, east=0)
        self.assertFalse(e._bbox_present())
        self.assertFalse(e._polyfile_present())
        self.assertRaisesRegex(ValidationError, r'incomplete .* boundaries', e.clean)

    def test_validation_raises_with_polyfile_and_incomplete_bbox(self):
        e = Extent(west=0, east=0, polyfile='present')
        self.assertFalse(e._bbox_present())
        self.assertTrue(e._polyfile_present())
        self.assertRaisesRegex(ValidationError, r'either .* or .* must be given|incomplete .* boundaries', e.clean)

    def test_validation_passes_with_bbox(self):
        e = Extent(west=0, south=0, east=0, north=0)
        self.assertTrue(e._bbox_present())
        self.assertFalse(e._polyfile_present())
        # no exception expected
        e.clean()

    def test_validation_passes_with_polyfile(self):
        e = Extent(polyfile='present')
        self.assertFalse(e._bbox_present())
        self.assertTrue(e._polyfile_present())
        # no exception expected
        e.clean()

    def test_get_geometry_returns_geometry(self):
        e = Extent(west=0, south=0, east=0, north=0)
        self.assertEqual(e.get_geometry().__dict__, BBox(west=0, south=0, east=0, north=0).__dict__)
        e.clean()

    def test_get_geometry_raises_with_polyfile_for_now(self):
        e = Extent(polyfile='present')
        self.assertRaises(NotImplementedError, e.get_geometry)
        e.clean()

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

    def test_output_directory_is_created_if_not_exists(self):
        conversion_job = ConversionJob()
        # need an id
        conversion_job.save()

        self.assertEqual(conversion_job.output_directory, '')