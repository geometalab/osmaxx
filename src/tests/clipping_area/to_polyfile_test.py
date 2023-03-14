import os
from unittest import TestCase

from django.contrib.gis.geos import MultiPolygon, Polygon, MultiLineString, LineString

from osmaxx.clipping_area.to_polyfile import create_poly_file_string
from osmaxx.utils.polyfile_helpers import parse_poly_string


class CreatePolyfileStringTest(TestCase):
    def setUp(self):
        self.poly_1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
        self.poly_2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
        self.multi_polygon_1 = MultiPolygon(self.poly_1, self.poly_2)
        self.multi_polygon_2 = MultiPolygon([self.poly_1, self.poly_2])

        self.holey_poly_3 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)), ((1, 1), (1, 2), (2, 2), (1, 1)))
        self.multi_polygon_3 = MultiPolygon(self.holey_poly_3)

    def test_create_poly_file_string_when_multipolygon_is_valid_returns_correct_string(self):
        result = create_poly_file_string(self.multi_polygon_1)
        expected = os.linesep.join([
            'none',
            '1-outer',
            '  0.000000000E+00 0.000000000E+00',
            '  0.000000000E+00 1.000000000E+00',
            '  1.000000000E+00 1.000000000E+00',
            '  0.000000000E+00 0.000000000E+00',
            'END',
            '2-outer',
            '  1.000000000E+00 1.000000000E+00',
            '  1.000000000E+00 2.000000000E+00',
            '  2.000000000E+00 2.000000000E+00',
            '  1.000000000E+00 1.000000000E+00',
            'END',
            'END',
            '',
        ])
        self.assertMultiLineEqual(expected, result)

    def test_create_poly_file_string_when_polygon_is_valid_returns_correct_string(self):
        expected = os.linesep.join([
            'none',
            '1-outer',
            '  0.000000000E+00 0.000000000E+00',
            '  0.000000000E+00 1.000000000E+00',
            '  1.000000000E+00 1.000000000E+00',
            '  0.000000000E+00 0.000000000E+00',
            'END',
            'END',
            '',
        ])
        result = create_poly_file_string(self.poly_1)
        self.assertMultiLineEqual(expected, result)

    def test_create_poly_file_string_when_valid_polygon_has_hole_returns_correct_string(self):
        expected = os.linesep.join([
            'none',
            '1-outer',
            '  0.000000000E+00 0.000000000E+00',
            '  0.000000000E+00 1.000000000E+00',
            '  1.000000000E+00 1.000000000E+00',
            '  0.000000000E+00 0.000000000E+00',
            'END',
            '!1-inner-1',
            '  1.000000000E+00 1.000000000E+00',
            '  1.000000000E+00 2.000000000E+00',
            '  2.000000000E+00 2.000000000E+00',
            '  1.000000000E+00 1.000000000E+00',
            'END',
            'END',
            '',
        ])
        result = create_poly_file_string(self.multi_polygon_3)
        self.assertMultiLineEqual(expected, result)

    def test_create_poly_file_string_when_input_is_invalid_raises_type_error(self):
        no_multi_polygon_at_all = 'asda'
        self.assertRaises(TypeError, create_poly_file_string, no_multi_polygon_at_all)

    def test_create_poly_file_string_when_geometry_is_invalid_raises_raises_type_error(self):
        invalid_geometry = MultiLineString(LineString((0, 0), (0, 1), (1, 1)), LineString((1, 1), (1, 2), (2, 2)))
        self.assertRaises(TypeError, create_poly_file_string, invalid_geometry)

    def test_create_poly_file_string_equals_the_multipolygon_it_was_constructed_from(self):
        ext_coords = ((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))
        int_coords = ((0.4, 0.4), (0.4, 0.6), (0.6, 0.6), (0.6, 0.4), (0.4, 0.4))
        complex_poly_3 = Polygon(ext_coords, int_coords)
        complex_multi_polygon = MultiPolygon(complex_poly_3, self.poly_1, self.poly_2)

        create_poly_file_string(self.multi_polygon_1)
        self.assertEqual(
            create_poly_file_string(self.multi_polygon_1),
            create_poly_file_string(parse_poly_string(create_poly_file_string(self.multi_polygon_1)))
        )
        self.assertEqual(
            create_poly_file_string(complex_multi_polygon),
            create_poly_file_string(parse_poly_string(create_poly_file_string(complex_multi_polygon)))
        )
