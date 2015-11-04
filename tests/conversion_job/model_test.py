from django.core.exceptions import ValidationError
from django.test import TestCase

from conversion_job.models import Extent


class ExtentTest(TestCase):
    def test_validation_raised_in_clean(self):
        e = Extent()
        print('poly: [', e.polyfile, '], west: [', e.west, ']')
        self.assertFalse(e._bbox_present())
        self.assertFalse(e._polyfile_present())
        self.assertRaises(ValidationError, e.clean)

    def test_validation_raises_when_both_present(self):
        e = Extent(west=0, south=0, east=0, north=0, polyfile='present')
        print('poly: [', e.polyfile, '], west: [', e.west, ']')
        self.assertTrue(e._bbox_present())
        self.assertTrue(e._polyfile_present())
        self.assertRaises(ValidationError, e.clean)

    def test_validation_passes_with_bbox(self):
        e = Extent(west=0, south=0, east=0, north=0)
        print('poly: [', e.polyfile, '], west: [', e.west, ']')
        self.assertTrue(e._bbox_present())
        self.assertFalse(e._polyfile_present())
        # no exception expected
        e.clean()

    def test_validation_passes_with_polyfile(self):
        e = Extent(polyfile='present')
        print('poly: [', e.polyfile, '], west: [', e.west, ']')
        self.assertFalse(e._bbox_present())
        self.assertTrue(e._polyfile_present())
        # no exception expected
        e.clean()
