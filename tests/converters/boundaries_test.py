import os
from unittest.mock import patch

from django.test import TestCase

from converters.boundaries import BBox, PolyfileForCountry, PolyfileCutter
from countries.models import Country
from tests.osm_test_helpers import POLYFILE_TEST_FILE_PATH


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
        'converters.converter_settings.OSMAXX_CONVERSION_SERVICE',
        PBF_PLANET_FILE_PATH='/path/to/planet-latest.osm.pbf',
    )
    @patch('subprocess.call', return_value=0)
    def test_cut_pbf_calls_osmconvert_correctly(self, sp_call_mock):
        # tests are using sample data from monaco
        bbox = BBox(west=1.23, south=-4.56, east=7.89, north=0.12)
        output_filename = 'outfile.pbf'
        bbox.cut_pbf(output_filename)
        sp_call_mock.assert_called_with(
            "osmconvert --out-pbf -o=outfile.pbf -b=1.23,-4.56,7.89,0.12 /path/to/planet-latest.osm.pbf".split(),
        )


class TestCountryPolyFile(TestCase):
    def test_init_when_parameters_are_missing_raises_type_error(self):
        self.assertRaises(TypeError, PolyfileForCountry)

    def test_initializing_when_all_given_parameters_are_set_works(self):
        poly_file_path = Country.objects.first().polyfile.path
        # shouldn't raise an error
        PolyfileForCountry(country_polyfile_path=poly_file_path)

    @patch.dict(
        'converters.converter_settings.OSMAXX_CONVERSION_SERVICE',
        PBF_PLANET_FILE_PATH='/path/to/planet-latest.osm.pbf',
    )
    @patch('subprocess.call', return_value=0)
    def test_cut_pbf_calls_osmconvert_correctly(self, sp_call_mock):
        # tests are using sample data from monaco
        poly_file_path = Country.objects.first().polyfile.path
        polyfile = PolyfileForCountry(country_polyfile_path=poly_file_path)
        output_filename = 'outfile.pbf'
        polyfile.cut_pbf(output_filename)
        sp_call_mock.assert_called_with(
            [
                "osmconvert",
                "--out-pbf",
                "-o=outfile.pbf",
                "-B={0}".format(POLYFILE_TEST_FILE_PATH),
                "/path/to/planet-latest.osm.pbf",
            ]
        )


# TODO: What if output filename contains spaces?
# TODO: What if path to planet file contains spaces?


class TestPolyfileCutter(TestCase):
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
        self.assertRaises(TypeError, PolyfileCutter)

    def test_init_when_invalid_poly_raises_error(self):
        self.assertRaises(TypeError, PolyfileCutter, self.example_invalid_poly_string)

    def test_initializing_when_all_given_parameters_are_set_works(self):
        PolyfileCutter(poly_string=self.example_valid_poly_string)
        # shouldn't raise an error

    @patch.dict(
        'converters.converter_settings.OSMAXX_CONVERSION_SERVICE',
        PBF_PLANET_FILE_PATH='/path/to/planet-latest.osm.pbf',
    )
    @patch('converters.boundaries.tempfile.NamedTemporaryFile')
    @patch('subprocess.call', return_value=0)
    def test_cut_pbf_calls_osmconvert_correctly(self, sp_call_mock, tmpfile_mock):
        expected_tmp_file_name = '/tmp/test_tmp_file_name'
        expected_output_file = 'outfile.pbf'
        expected_pbf_path = '/path/to/planet-latest.osm.pbf'
        tmpfile_mock.return_value.__enter__.return_value.name = expected_tmp_file_name

        polyfile = PolyfileCutter(poly_string=self.example_valid_poly_string)
        polyfile.cut_pbf(expected_output_file)
        sp_call_mock.assert_called_with(
            [
                "osmconvert",
                "--out-pbf",
                "-o={}".format(expected_output_file),
                "-B={}".format(expected_tmp_file_name),
                "{}".format(expected_pbf_path),
            ]
        )
