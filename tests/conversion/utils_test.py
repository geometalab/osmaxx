import os
import shutil
import tempfile

import pytest

from osmaxx.conversion.converters.utils import recursive_getsize


@pytest.fixture
def directory_with_subdirectories(request):
    tempdir = tempfile.TemporaryDirectory()

    def rm_tmpdir():
        shutil.rmtree(tempdir.name)
    request.addfinalizer(rm_tmpdir)

    file_sizes = [102, 304, 10, 2000, 10, 678691, 1667, 1254]
    expected_size = sum(file_sizes)
    subdir = tempdir.name
    for index, file_size in enumerate(file_sizes):
        if index % 2 == 0:
            subdir = os.path.join(subdir, str(file_size))
            os.mkdir(subdir)
        elif index != 0:
            subdir = os.path.join(subdir, str(index))
            os.mkdir(subdir)
        file_path = os.path.join(subdir, 'example_{}.file'.format(str(file_size)))
        with open(file_path, 'w') as file:
            file.truncate(file_size)
        assert os.path.getsize(file_path) == file_size
    return tempdir.name, expected_size


def test_recursive_getsize_does_count_subdirectories(directory_with_subdirectories):
    directory, expected_size = directory_with_subdirectories
    assert recursive_getsize(directory) == expected_size
