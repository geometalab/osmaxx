import string
import random
from django.test import TestCase
import os
from osmaxx.utils import PrivateSystemStorage


class PrivateSystemStorageTestCase(TestCase):
    def setUp(self):
        random_directory_name_length = 10
        self.random_directory_name = ''.join(
            random.choice(string.ascii_lowercase + string.digits) for _throwaway in range(random_directory_name_length)
        )

    def test_creates_a_new_directory_if_it_does_not_exist(self):
        random_directory_path = os.path.join('/tmp/', self.random_directory_name)
        self.assertFalse(os.path.exists(random_directory_path))
        PrivateSystemStorage(location=random_directory_path)
        self.assertTrue(os.path.exists(random_directory_path))
        os.rmdir(random_directory_path)

    def xtest_raises_when_missing_permissions(self):
        # FIXME: this isn't testable as it stands, because we are root on the docker instance
        #        and it will overwrite the access rights to create a directory.
        read_only_directory = os.path.join('/tmp/', 'read_only_dir')
        os.mkdir(read_only_directory, mode=0o000)
        random_directory_path = os.path.join(read_only_directory, self.random_directory_name)
        self.assertFalse(os.path.exists(random_directory_path))
        with self.assertRaises(OSError):
            PrivateSystemStorage(location=random_directory_path)
        self.assertFalse(os.path.exists(random_directory_path))
