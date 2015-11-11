from django.conf import settings
from django.test import TestCase

from file_size_estimation.estimate_size import estimate_size_of_extent


class EstimateSizeTest(TestCase):
    csv_file_name = settings.OSMAXX_CONVERSION_SERVICE['ESTIMATION_CSV_SOURCE_FILE']

    def test_monaco_size_estimation(self):
        monaco_bbox = [7.400, 43.717, 7.439, 43.746]
        self.assertEqual(estimate_size_of_extent(self.csv_file_name, *monaco_bbox), 33735)

    def test_dateline_overlap_should_work(self):
        dateline_bbox = [160, 43.717, -160, 43.746]
        self.assertEqual(estimate_size_of_extent(self.csv_file_name, *dateline_bbox), 291)

    def test_dateline_overlap_should_equal_the_two_adjecent_bboxes(self):
        dateline_bbox = [160, 43.717, -160, 43.746]
        dateline_east_side_bbox = [160, 43.717, 180, 43.746]
        dateline_west_side_bbox = [-180, 43.717, -160, 43.746]

        self.assertEqual(
            estimate_size_of_extent(self.csv_file_name, *dateline_bbox),
            estimate_size_of_extent(self.csv_file_name, *dateline_east_side_bbox) +
            estimate_size_of_extent(self.csv_file_name, *dateline_west_side_bbox)
        )

    def test_north_cant_be_greater_than_south(self):
        south_greater_than_north_bbox = [8, 44, 9, 43]
        self.assertRaises(
            ArithmeticError,
            estimate_size_of_extent,
            self.csv_file_name,
            *south_greater_than_north_bbox
        )

    def test_out_of_bounds_extent(self):
        # list: west, south, east, north
        west_too_big = [180.1, 2, 3, 4]
        west_too_small = [-180.1, 2, 3, 4]
        south_too_big = [1, 90.1, 3, 4]
        south_too_small = [1, -90.1, 3, 4]
        east_too_big = [1, 2, 180.1, 4]
        east_too_small = [1, 2, -180.1, 4]
        north_too_big = [1, 2, 3, 90.1]
        north_too_small = [1, 2, 3, -90.1]

        out_of_bounds_extents = [
            west_too_big, west_too_small,
            south_too_big, south_too_small,
            east_too_big, east_too_small,
            north_too_big, north_too_small,
        ]

        for extent in out_of_bounds_extents:
            self.assertRaises(
                ArithmeticError,
                estimate_size_of_extent,
                self.csv_file_name,
                *extent
            )
