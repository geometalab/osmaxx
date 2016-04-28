import os
import tempfile
import shutil

from django.test import TestCase

from osmaxx.utils.directory_helper import get_file_only_path_list_in_directory


class GetFileListInDirectoryTest(TestCase):
    def setUp(self):
        self.random_directory = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.random_directory)

    def _create_dirs_and_files_in_dir(self, dirs=(), file_names=()):
        if dirs:
            for directory in dirs:
                os.mkdir(os.path.join(self.random_directory, directory))
        if file_names:
            for filename in file_names:
                open(os.path.join(self.random_directory, filename), 'x').close()

    def _get_file_list_sorted_with_random_dir_prepended(self, file_names):
        result_list = [os.path.join(self.random_directory, file_name) for file_name in file_names]
        result_list.sort()
        return result_list

    def test_get_file_only_path_list_in_directory_lists_all_files(self):
        file_names = ['test1.test', 'test2.txt', '_no_extension_test3']
        self._create_dirs_and_files_in_dir(file_names=file_names)

        path_list_from_get_file_only_path = get_file_only_path_list_in_directory(self.random_directory)
        path_list_from_get_file_only_path.sort()

        self.assertListEqual(
            path_list_from_get_file_only_path,
            self._get_file_list_sorted_with_random_dir_prepended(file_names=file_names)
        )

    def test_get_file_only_path_list_in_directory_lists_no_directories(self):
        directories = ['testdir1', 'directory2', '_some_other_dir']
        file_names = ['test1.test', 'test2.txt', '_no_extension_test3']
        self._create_dirs_and_files_in_dir(dirs=directories, file_names=file_names)

        path_list_from_get_file_only_path = get_file_only_path_list_in_directory(self.random_directory)
        path_list_from_get_file_only_path.sort()

        self.assertListEqual(
            path_list_from_get_file_only_path,
            self._get_file_list_sorted_with_random_dir_prepended(file_names=file_names)
        )

    def test_get_file_only_path_list_in_directory_fails_if_directory_does_not_exist(self):
        shutil.rmtree(self.random_directory)
        self.assertRaises(FileNotFoundError, get_file_only_path_list_in_directory, self.random_directory)
        # don't let teardown fail!
        os.mkdir(self.random_directory)

    def test_get_file_only_path_list_in_directory_returns_empty_list_if_directory_is_empty(self):
        self.assertListEqual(get_file_only_path_list_in_directory(self.random_directory), [])

    def test_get_file_only_path_list_in_directory_returns_empty_list_if_directory_contains_only_directories(self):
        directories = ['testdir1', 'directory2', '_some_other_dir']
        self._create_dirs_and_files_in_dir(dirs=directories)

        path_list_from_get_file_only_path = get_file_only_path_list_in_directory(self.random_directory)
        path_list_from_get_file_only_path.sort()

        self.assertListEqual(
            path_list_from_get_file_only_path,
            self._get_file_list_sorted_with_random_dir_prepended(file_names=[])
        )

    def test_get_file_only_path_list_in_directory_does_not_recurse(self):
        directories = ['testdir1', 'directory2', '_some_other_dir']
        self._create_dirs_and_files_in_dir(dirs=directories, file_names=[])
        file_names_in_subdir = ['test1.test', 'test2.txt', '_no_extension_test3']
        for directory in directories:
            for file_name in file_names_in_subdir:
                open(os.path.join(self.random_directory, directory, file_name), 'x').close()
        self.assertListEqual(get_file_only_path_list_in_directory(self.random_directory), [])
