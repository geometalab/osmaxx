from django.test import TestCase
from django.contrib.auth.models import User
from osmaxx.contrib.auth.frontend_permissions import user_in_osmaxx_group


class TestFrontendPermissions(TestCase):
    def test_superuser_can_access_frontend_even_if_not_in_osmaxx_group(self):
        an_admin = User.objects.create_superuser('A. D. Min', 'admin@example.com', 'password')
        self.assertTrue(user_in_osmaxx_group(an_admin))
