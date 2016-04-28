import os
import shutil

from django.test import TestCase

from osmaxx.utils import PrivateSystemStorage


class PrivateSystemStorageTestCase(TestCase):
    def setUp(self):
        self.directory_name = 'OSMAXX_private-storage-directory-for-tests'

    def test_creates_a_new_directory_if_it_does_not_exist(self):
        directory_path = os.path.join('/tmp/', self.directory_name)
        self.assertFalse(os.path.exists(directory_path))
        PrivateSystemStorage(location=directory_path)
        self.assertTrue(os.path.exists(directory_path))
        os.rmdir(directory_path)

    def test_raises_when_missing_permissions(self):
        read_only_directory = os.path.join('/tmp/', 'read_only_dir')
        os.mkdir(read_only_directory, mode=0o0444)
        try:
            directory_path = os.path.join(read_only_directory, self.directory_name)
            self.assertFalse(os.path.exists(directory_path))
            with self.assertRaises(OSError):
                PrivateSystemStorage(location=directory_path)
            self.assertFalse(os.path.exists(directory_path))
        finally:
            shutil.rmtree(read_only_directory)
