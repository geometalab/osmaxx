# Monaco
import os

from tests.conftest import test_data_dir

BOUNDING_BOX_TEST_OSM = {
    'west': 7.400,  # (min lon)
    'south': 43.717,  # (min lat)
    'east': 7.439,  # (max lon)
    'north': 43.746,  # (max lat)
}

# Monaco Polyfile
POLYFILE_TEST_FILE_PATH = os.path.join(test_data_dir, 'osm', 'monaco.poly')
