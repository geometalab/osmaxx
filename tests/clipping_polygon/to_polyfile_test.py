from unittest import TestCase

from django.contrib.gis.geos import MultiPolygon, Polygon, MultiLineString, LineString

from clipping_geometry.to_polyfile import create_poly_file_string


class CreatePolyfileStringTest(TestCase):
    def setUp(self):
        self.poly_1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
        self.poly_2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
        self.multi_polygon_1 = MultiPolygon(self.poly_1, self.poly_2)
        self.multi_polygon_2 = MultiPolygon([self.poly_1, self.poly_2])

    def test_create_poly_file_string_when_valid_multipolygon_returns_correct_string(self):
        result = create_poly_file_string(self.multi_polygon_1)
        expected = '\n'.join([
            'none',
            '1',
            '  0.000000E+00 0.000000E+00',
            '  0.000000E+00 1.000000E+00',
            '  1.000000E+00 1.000000E+00',
            '  0.000000E+00 0.000000E+00',
            'END',
            '2',
            '  1.000000E+00 1.000000E+00',
            '  1.000000E+00 2.000000E+00',
            '  2.000000E+00 2.000000E+00',
            '  1.000000E+00 1.000000E+00',
            'END',
            'END',
            '',
        ])
        self.assertMultiLineEqual(expected, result)

    def test_create_poly_file_string_when_valid_polygon_returns_correct_string(self):
        expected = '\n'.join([
            'none',
            '1',
            '  0.000000E+00 0.000000E+00',
            '  0.000000E+00 1.000000E+00',
            '  1.000000E+00 1.000000E+00',
            '  0.000000E+00 0.000000E+00',
            'END',
            'END',
            '',
        ])
        result = create_poly_file_string(self.poly_1)
        self.assertMultiLineEqual(expected, result)

    def test_create_poly_file_string_when_invalid_input_raises_type_error(self):
        no_multi_polygon_at_all = 'asda'
        self.assertRaises(TypeError, create_poly_file_string, no_multi_polygon_at_all)

    def test_create_poly_file_string_when_invalid_geometry_raises_type_error(self):
        invalid_geometry = MultiLineString(LineString((0, 0), (0, 1), (1, 1)), LineString((1, 1), (1, 2), (2, 2)))
        self.assertRaises(TypeError, create_poly_file_string, invalid_geometry)
