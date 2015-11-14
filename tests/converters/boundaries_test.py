from unittest.mock import patch

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

    @patch.dict('converters.converter_settings.OSMAXX_CONVERSION_SERVICE', {
        'PBF_PLANET_FILE_PATH': '/path/to/planet-latest.osm.pbf',
    })
    # FIXME: _get_cut_command should also be sensitive to overriding django.conf.settings.OSMAXX_CONVERSION_SERVICE
    #        but it isn't.
    def test_get_cut_command_returns_expected_command(self, *args, **kwargs):
        expected = "osmconvert --out-pbf -o=outfile.pbf -b=1.23,-4.56,7.89,0.12 /path/to/planet-latest.osm.pbf"
        bbox = BBox(west=1.23, south=-4.56, east=7.89, north=0.12)
        actual = bbox._get_cut_command(output_filename='outfile.pbf')
        self.assertEqual(expected, actual)
