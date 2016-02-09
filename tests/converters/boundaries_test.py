import os
from unittest import mock
from unittest.mock import patch

from django.test import TestCase

from osmaxx.converters.boundaries import BBox, BoundaryCutter, pbf_area


class TestBBox(TestCase):
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

    @patch.dict(
        'osmaxx.converters.converter_settings.OSMAXX_CONVERSION_SERVICE',
        PBF_PLANET_FILE_PATH='/path/to/planet-latest.osm.pbf',
    )
    @patch('subprocess.call', return_value=0)
    def test_cut_pbf_calls_subprocess(self, sp_call_mock):
        # tests are using sample data from monaco
        bbox = BBox(west=1.23, south=-4.56, east=7.89, north=0.12)
        output_filename = 'outfile.pbf'
        bbox.cut_pbf(output_filename)
        sp_call_mock.assert_called_with(
            "osmconvert --out-pbf -o=outfile.pbf -b=1.23,-4.56,7.89,0.12 /path/to/planet-latest.osm.pbf".split(),
        )


# TODO: What if output filename contains spaces?
# TODO: What if path to planet file contains spaces?


class TestPBFArea(TestCase):
    def setUp(self):
        self.example_valid_poly_string = os.linesep.join([
            'australia_v',
            '1',
            '     0.1446693E+03    -0.3826255E+02',
            '     0.1446763E+03    -0.3825659E+02',
            '     0.1446627E+03    -0.3825661E+02',
            '     0.1446763E+03    -0.3824465E+02',
            '     0.1446813E+03    -0.3824343E+02',
            '     0.1446824E+03    -0.3824484E+02',
            '     0.1446826E+03    -0.3825356E+02',
            '     0.1446876E+03    -0.3825210E+02',
            '     0.1446919E+03    -0.3824719E+02',
            '     0.1447006E+03    -0.3824723E+02',
            '     0.1447042E+03    -0.3825078E+02',
            '     0.1446758E+03    -0.3826229E+02',
            '     0.1446693E+03    -0.3826255E+02',
            'END',
            '!2',
            '     0.1422436E+03    -0.3839315E+02',
            '     0.1422483E+03    -0.3839481E+02',
            '     0.1422496E+03    -0.3839070E+02',
            '     0.1422543E+03    -0.3839025E+02',
            '     0.1422574E+03    -0.3839155E+02',
            '     0.1422467E+03    -0.3840065E+02',
            '     0.1422433E+03    -0.3840048E+02',
            '     0.1422420E+03    -0.3839857E+02',
            '     0.1422436E+03    -0.3839315E+02',
            'END',
            'END',
        ])

        self.example_invalid_poly_string = os.linesep.join([
            'australia_v',
            '1',
            'END',
            'END',
            'END',
        ])

    def test_init_when_parameters_are_missing_raises_type_error(self):
        self.assertRaises(TypeError, pbf_area)

    def test_init_when_invalid_poly_raises_error(self):
        self.assertRaises(TypeError, pbf_area, self.example_invalid_poly_string)

    def test_initializing_when_all_given_parameters_are_set_works(self):
        pbf_area(osmosis_polygon_file_content=self.example_valid_poly_string)
        # shouldn't raise an error

    @patch.dict(
        'osmaxx.converters.converter_settings.OSMAXX_CONVERSION_SERVICE',
        PBF_PLANET_FILE_PATH='/path/to/planet-latest.osm.pbf',
    )
    @patch('subprocess.call', return_value=0)
    def test_cut_pbf_calls_osmconvert(self, sp_call_mock, *args):
        with pbf_area(osmosis_polygon_file_content=self.example_valid_poly_string):
            sp_call_mock.assert_called_once_with(mock.ANY)

    @patch.dict(
        'osmaxx.converters.converter_settings.OSMAXX_CONVERSION_SERVICE',
        PBF_PLANET_FILE_PATH='/path/to/planet-latest.osm.pbf',
    )
    @patch('subprocess.call', return_value=0)
    def test_cut_pbf_cleans_up_temp_files(self, *args):
        with pbf_area(osmosis_polygon_file_content=self.example_valid_poly_string) as pbf_file_path:
            self.assertTrue(os.path.exists(pbf_file_path))
        self.assertFalse(os.path.exists(pbf_file_path))


class TestBoundaryCutter(TestCase):
    @patch('subprocess.check_call', return_value=0)
    def test_cut_pbf_is_called_correctly(self, check_call_mock):
        expected_osmosis_polygon_file_path = '/test/path/to_fake_polygon_file'
        expected_input_pbf = '/fake/path/to/pbf/input'
        expected_output_pbf = '/fake/path/to/pbf/output'

        boundary_cutter = BoundaryCutter(expected_osmosis_polygon_file_path)
        boundary_cutter.cut_pbf(input_pbf=expected_input_pbf, output_pbf=expected_output_pbf)
        check_call_mock.assert_called_once_with([
            "osmconvert",
            "--out-pbf",
            "-o={0}".format(expected_output_pbf),
            "-B={0}".format(expected_osmosis_polygon_file_path),
            "{0}".format(expected_input_pbf),
        ])
