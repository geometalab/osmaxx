from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from converters.boundaries import BBox


class TestBBox(TestCase):
    def setUp(self):
        self.boundary = BBox(west=0, south=0, east=0, north=0)

    def test_init_when_parameters_are_missing_raises_type_error(self):
        self.assertRaises(TypeError, BBox, west=0, south=0, east=0)
        self.assertRaises(TypeError, BBox, west=0, south=0, north=0)
        self.assertRaises(TypeError, BBox, west=0, east=0, north=0)
        self.assertRaises(TypeError, BBox, south=0, east=0, north=0)
        self.assertRaises(TypeError, BBox, north=0)
        self.assertRaises(TypeError, BBox, east=0)
        self.assertRaises(TypeError, BBox, south=0)
        self.assertRaises(TypeError, BBox, west=0)

    def test_initializing_when_all_given_parameters_are_set_works(self):
        # shouldn't raise an error
        BBox(west=0, south=0, east=0, north=0)

    @patch('converters.boundaries.BBox._get_cut_command', return_value='true')
    def test_cut_pbf_calls_correctly(self, cut_command_mock):
        # tests are using sample data from monaco
        bbox = BBox(west=1.23, south=-4.56, east=7.89, north=0.12)
        output_filename = 'cutted_filename.pbf'
        bbox.cut_pbf(output_filename)
        cut_command_mock.assertCalledWith(
            output_filename=output_filename
        )

    def test_get_cut_command_returns_expected_command(self):
        pbf_file_path = settings.OSMAXX_CONVERSION_SERVICE.get('PBF_PLANET_FILE_PATH')
        expected = "osmconvert --out-pbf -o=cutted_filename.pbf -b=1.23,-4.56,7.89,0.12 {pbf_file_path}".format(
            pbf_file_path=pbf_file_path,
        )
        bbox = BBox(west=1.23, south=-4.56, east=7.89, north=0.12)
        actual = bbox._get_cut_command(output_filename='cutted_filename.pbf')
        self.assertEqual(expected, actual)
