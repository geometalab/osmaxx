import os

import pytest

from osmaxx.conversion.converters.converter_garmin import garmin

relative_library_names = [
    'command_line_utils/mkgmap/mkgmap.jar',
    'command_line_utils/mkgmap/lib/fastutil-6.5.15-mkg.1b.jar',
    'command_line_utils/mkgmap/lib/osmpbf-1.3.3.jar',
    'command_line_utils/mkgmap/lib/protobuf-java-2.5.0.jar',
    'command_line_utils/splitter/splitter.jar',
    'command_line_utils/splitter/lib/fastutil-6.5.15-mkg.1b.jar',
    'command_line_utils/splitter/lib/osmpbf-1.3.3.jar',
    'command_line_utils/splitter/lib/protobuf-java-2.5.0.jar',
    'command_line_utils/splitter/lib/xpp3-1.1.4c.jar',
]


@pytest.fixture(params=relative_library_names)
def library_path(request):
    search_base_path = os.path.abspath(os.path.dirname(garmin.__file__))
    return os.path.join(search_base_path, request.param)


def test_libraries_are_contained_in_source(library_path):
    assert os.path.exists(library_path)
