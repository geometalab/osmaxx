from django.test import TestCase
from django.contrib.auth.models import User, Group
from osmaxx.contrib.auth.frontend_permissions import user_in_osmaxx_group, FRONTEND_USER_GROUP


class TestFrontendPermissions(TestCase):
    def test_user_can_not_access_frontend_by_default(self):
        a_user = User.objects.create_user('U. Ser', 'user@example.com', 'password')
        self.assertFalse(user_in_osmaxx_group(a_user))

    def test_user_can_access_frontend_when_in_osmaxx_group(self):
        a_user = User.objects.create_user('U. Ser', 'user@example.com', 'password')
        a_user.groups.add(Group.objects.get(name=FRONTEND_USER_GROUP))
        self.assertTrue(user_in_osmaxx_group(a_user))

    def test_superuser_can_access_frontend_even_if_not_in_osmaxx_group(self):
        an_admin = User.objects.create_superuser('A. D. Min', 'admin@example.com', 'password')
        self.assertTrue(user_in_osmaxx_group(an_admin))
