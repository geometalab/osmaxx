from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from converters.boundaries import BBox
from tests.osm_test_helpers import BOUNDING_BOX_TEST_OSM


class TestBBox(TestCase):
    def setUp(self):
        self.boundary = BBox(west=0, south=0, east=0, north=0)

    def test_init_complains_when_parameters_are_missing(self):
        self.assertRaises(TypeError, BBox, west=0, south=0, east=0)
        self.assertRaises(TypeError, BBox, west=0, south=0, north=0)
        self.assertRaises(TypeError, BBox, west=0, east=0, north=0)
        self.assertRaises(TypeError, BBox, south=0, east=0, north=0)
        self.assertRaises(TypeError, BBox, north=0)
        self.assertRaises(TypeError, BBox, east=0)
        self.assertRaises(TypeError, BBox, south=0)
        self.assertRaises(TypeError, BBox, west=0)

    def test_initializing_works_if_all_given_parameters_are_set(self):
        # shouldn't raise an error
        BBox(west=0, south=0, east=0, north=0)

    @patch('converters.boundaries.BBox._get_cut_command', return_value='true')
    def test_cut_pbf_calls_correctly(self, cut_command_mock):
        # tests are using sample data from monaco
        bbox = BBox(**BOUNDING_BOX_TEST_OSM)
        output_filename = 'cutted_filename.pbf'
        bbox.cut_pbf(output_filename)
        cut_command_mock.assertCalledWith(
            output_filename=output_filename
        )

    def test_get_cut_command_returns_expected_command(self):
        output_filename = 'cutted_filename.pbf'
        pbf_file_path = settings.OSMAXX_CONVERSION_SERVICE.get('PBF_WORLD_FILE_PATH')
        expected = "osmconvert --out-pbf -o={output_filename} -b={west},{south},{east},{north} {pbf_file_path}".format(
            output_filename=output_filename,
            pbf_file_path=pbf_file_path,
            west=BOUNDING_BOX_TEST_OSM['west'],
            south=BOUNDING_BOX_TEST_OSM['south'],
            east=BOUNDING_BOX_TEST_OSM['east'],
            north=BOUNDING_BOX_TEST_OSM['north'],
        )
        bbox = BBox(**BOUNDING_BOX_TEST_OSM)
        actual = bbox._get_cut_command(output_filename=output_filename)
        self.assertEqual(expected, actual)
