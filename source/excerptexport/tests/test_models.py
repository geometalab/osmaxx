from django.test.testcases import TestCase
from excerptexport.models.bounding_geometry import BoundingGeometry


class BoundingGeometryTestCase(TestCase):
    def test_create_from_bounding_box_coordinates_persists_new_bounding_geo(self):
        BoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertEqual(BoundingGeometry.objects.count(), 1)

    def test_create_from_bounding_box_coordinates_produces_only_exterior_ring(self):
        BoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertEqual(BoundingGeometry.objects.first().geometry.num_interior_rings, 0)

    def test_create_from_bounding_box_coordinates_produces_exterior_ring_with_5_points(self):
        BoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertEqual(BoundingGeometry.objects.first().geometry.exterior_ring.num_points, 5)

    def test_create_from_bounding_box_coordinates_produces_closed_exterior_ring(self):
        BoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        exterior_ring = BoundingGeometry.objects.first().geometry.exterior_ring
        self.assertEqual(exterior_ring[0], exterior_ring[-1])

    def test_create_from_bounding_box_coordinates_contains_north_east_corner(self):
        BoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertIn((2.2, 1.1), BoundingGeometry.objects.first().geometry.exterior_ring)

    def test_create_from_bounding_box_coordinates_contains_south_east_corner(self):
        BoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertIn((2.2, 3.3), BoundingGeometry.objects.first().geometry.exterior_ring)

    def test_create_from_bounding_box_coordinates_contains_north_west_corner(self):
        BoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertIn((4.4, 1.1), BoundingGeometry.objects.first().geometry.exterior_ring)

    def test_create_from_bounding_box_coordinates_contains_south_west_corner(self):
        BoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertIn((4.4, 3.3), BoundingGeometry.objects.first().geometry.exterior_ring)

    def test_create_from_bounding_box_coordinates_produces_clockwise_exterior_ring_starting_at_south_west(self):
        BoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertEqual(BoundingGeometry.objects.first().geometry.exterior_ring[:],
                         [(4.4, 3.3), (4.4, 1.1), (2.2, 1.1), (2.2, 3.3), (4.4, 3.3)])
