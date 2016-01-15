import json

from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from osmaxx.excerptexport.models.bounding_geometry import BoundingGeometry, BBoxBoundingGeometry
from osmaxx.excerptexport import models


class BBoxBoundingGeometryTestCase(TestCase):
    def test_create_from_bounding_box_coordinates_persists_new_bounding_geo(self):
        BBoxBoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertEqual(BoundingGeometry.objects.count(), 1)

    def test_geometry_has_only_exterior_ring(self):
        BBoxBoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertEqual(BoundingGeometry.objects.first().bboxboundinggeometry.geometry.num_interior_rings, 0)

    def test_geometry_has_exterior_ring_with_5_points(self):
        BBoxBoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertEqual(BoundingGeometry.objects.first().bboxboundinggeometry.geometry.exterior_ring.num_points, 5)

    def test_geometry_has_closed_exterior_ring(self):
        BBoxBoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        exterior_ring = BoundingGeometry.objects.first().bboxboundinggeometry.geometry.exterior_ring
        self.assertEqual(exterior_ring[0], exterior_ring[-1])

    def test_geometry_contains_north_east_corner(self):
        BBoxBoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertIn((2.2, 1.1), BoundingGeometry.objects.first().bboxboundinggeometry.geometry.exterior_ring)

    def test_geometry_contains_south_east_corner(self):
        BBoxBoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertIn((2.2, 3.3), BoundingGeometry.objects.first().bboxboundinggeometry.geometry.exterior_ring)

    def test_geometry_contains_north_west_corner(self):
        BBoxBoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertIn((4.4, 1.1), BoundingGeometry.objects.first().bboxboundinggeometry.geometry.exterior_ring)

    def test_geometry_contains_south_west_corner(self):
        BBoxBoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertIn((4.4, 3.3), BoundingGeometry.objects.first().bboxboundinggeometry.geometry.exterior_ring)

    def test_geometry_has_clockwise_exterior_ring_starting_at_south_west(self):
        BBoxBoundingGeometry.create_from_bounding_box_coordinates(1.1, 2.2, 3.3, 4.4)
        self.assertEqual(BoundingGeometry.objects.first().bboxboundinggeometry.geometry.exterior_ring[:],
                         [(4.4, 3.3), (4.4, 1.1), (2.2, 1.1), (2.2, 3.3), (4.4, 3.3)])


class ExtractionOrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'pw')
        self.excerpt = models.Excerpt.objects.create(
            name='Neverland',
            is_active=True,
            is_public=False,
            owner=self.user,
            bounding_geometry=models.OsmosisPolygonFilterBoundingGeometry.objects.create(
                polygon_file=SimpleUploadedFile('in_memory_file.poly', b'the file content (not a real .poly file)')
            )
        )
        self.extraction_configuration = {
            'gis_formats': ['txt'],
            'gis_options': {
                'detail_level': 'standard'
            }
        }

    def test_create_and_restore_extraction_configuration(self):
        extraction_order_id = models.ExtractionOrder.objects.create(
            excerpt=self.excerpt,
            orderer=self.user,
            extraction_configuration={'gis_formats': ['txt'], 'gis_options': {'detail_level': 'standard'}}
        ).id
        extraction_order = models.ExtractionOrder.objects.get(pk=extraction_order_id)
        self.assertEqual(extraction_order.extraction_configuration, self.extraction_configuration)

    def test_persistence_representation_is_json(self):
        extraction_order_id = models.ExtractionOrder.objects.create(
            excerpt=self.excerpt,
            orderer=self.user,
            extraction_configuration={'gis_formats': ['txt'], 'gis_options': {'detail_level': 'standard'}}
        ).id
        extraction_order = models.ExtractionOrder.objects.get(pk=extraction_order_id)
        self.assertEqual(extraction_order._extraction_configuration, json.dumps(self.extraction_configuration))
