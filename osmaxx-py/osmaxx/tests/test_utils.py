import os

from django.test import TestCase

from osmaxx.utils import PrivateSystemStorage


class PrivateSystemStorageTestCase(TestCase):
    def setUp(self):
        self.directory_name = 'OSMAXX_OjM3cRB2xgSuDXr5yBxxzds9mO8gmP'

    def test_creates_a_new_directory_if_it_does_not_exist(self):
        directory_path = os.path.join('/tmp/', self.directory_name)
        self.assertFalse(os.path.exists(directory_path))
        PrivateSystemStorage(location=directory_path)
        self.assertTrue(os.path.exists(directory_path))
        os.rmdir(directory_path)

    def xtest_raises_when_missing_permissions(self):
        # FIXME: this isn't testable as it stands, because we are root on the docker instance
        #        and it will overwrite the access rights to create a directory.
        read_only_directory = os.path.join('/tmp/', 'read_only_dir')
        os.mkdir(read_only_directory, mode=0o000)
        directory_path = os.path.join(read_only_directory, self.directory_name)
        self.assertFalse(os.path.exists(directory_path))
        with self.assertRaises(OSError):
            PrivateSystemStorage(location=directory_path)
        self.assertFalse(os.path.exists(directory_path))
