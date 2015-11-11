# Monaco
import os

from tests.conftest import test_data_dir

BOUNDING_BOX_TEST_OSM = {
    'west': 7.400,
    'east': 43.717,
    'south': 7.439,
    'north': 43.746,
}

# Monaco Polyfile
POLYFILE_TEST_FILE_PATH = os.path.join(test_data_dir, 'osm', 'monaco.poly')
