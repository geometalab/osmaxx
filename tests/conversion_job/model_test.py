from django.core.exceptions import ValidationError
from django.test import TestCase

from conversion_job.models import Extent


class ExtentTest(TestCase):
    def test_validation_raised_in_clean(self):
        e = Extent()
        self.assertFalse(e._bbox_present())
        self.assertFalse(e._polyfile_present())
        self.assertRaisesRegex(ValidationError, 'either .* or .* must be given', e.clean)

    def test_validation_raises_when_both_present(self):
        e = Extent(west=0, south=0, east=0, north=0, polyfile='present')
        self.assertTrue(e._bbox_present())
        self.assertTrue(e._polyfile_present())
        self.assertRaisesRegex(ValidationError, 'either .* or .* must be given', e.clean)

    def test_validation_raises_with_incomplete_bbox(self):
        e = Extent(west=0, east=0)
        self.assertFalse(e._bbox_present())
        self.assertFalse(e._polyfile_present())
        self.assertRaises(ValidationError, e.clean)

    def test_validation_raises_with_polyfile_and_incomplete_bbox(self):
        e = Extent(west=0, east=0, polyfile='present')
        self.assertFalse(e._bbox_present())
        self.assertTrue(e._polyfile_present())
        self.assertRaises(ValidationError, e.clean)

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
