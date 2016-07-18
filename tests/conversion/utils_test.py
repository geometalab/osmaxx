import os
import shutil
import tempfile

import pytest

from osmaxx.conversion.converters.utils import recursive_getsize


@pytest.fixture
def directory_with_subdirectories(request):
    """
    This creates the following file and directory structure
    <tmpdir>
        ├── 102
        │   ├── 304
        │   │   ├── 10
        │   │   │   ├── 2000
        │   │   │   │   ├── 10
        │   │   │   │   │   ├── 678691
        │   │   │   │   │   │   ├── 1667
        │   │   │   │   │   │   │   ├── 1254
        │   │   │   │   │   │   │   │   └── example_1254.file
        │   │   │   │   │   │   │   ├── empty_dir
        │   │   │   │   │   │   │   └── example_1667.file
        │   │   │   │   │   │   ├── empty_dir
        │   │   │   │   │   │   └── example_678691.file
        │   │   │   │   │   ├── empty_dir
        │   │   │   │   │   └── example_10.file
        │   │   │   │   ├── empty_dir
        │   │   │   │   └── example_2000.file
        │   │   │   ├── empty_dir
        │   │   │   └── example_10.file
        │   │   ├── empty_dir
        │   │   └── example_304.file
        │   ├── empty_dir
        │   └── example_102.file
        └── empty_dir
    """
    tempdir = tempfile.TemporaryDirectory()

    def rm_tmpdir():
        shutil.rmtree(tempdir.name)
    request.addfinalizer(rm_tmpdir)

    file_sizes = [102, 304, 10, 2000, 10, 678691, 1667, 1254]
    expected_size = sum(file_sizes)
    subdir = tempdir.name
    for file_size in file_sizes:
        os.mkdir(os.path.join(subdir, 'empty_dir'))
        subdir = os.path.join(subdir, str(file_size))
        os.mkdir(subdir)

        file_path = os.path.join(subdir, 'example_{}.file'.format(str(file_size)))
        with open(file_path, 'w') as file:
            file.truncate(file_size)
        assert os.path.getsize(file_path) == file_size
    return tempdir.name, expected_size


def test_recursive_getsize_sums_up_sizes_correctly_with_subdirectories(directory_with_subdirectories):
    directory, expected_size = directory_with_subdirectories
    assert recursive_getsize(directory) == expected_size
