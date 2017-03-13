from django.conf import settings
from django.contrib.auth.models import User, Group
from osmaxx.contrib.auth.frontend_permissions import _may_user_access_osmaxx_frontend


def test_user_can_not_access_frontend_by_default(db):
    """
    Newly created users (self sign-up) can't do anything that non-authenticated visitors couldn't do, too, so that
    we don't have to restrict who can sign up.
    """
    a_user = User.objects.create_user('U. Ser', 'user@example.com', 'password')
    assert not _may_user_access_osmaxx_frontend(a_user)


def test_user_can_access_frontend_when_in_osmaxx_group(db):
    """
    To activate a user for frontend access, add it to the osmaxx frontend group.
    """
    a_user = User.objects.create_user('U. Ser', 'user@example.com', 'password')
    a_user.groups.add(Group.objects.get(name=settings.OSMAXX_FRONTEND_USER_GROUP))
    assert _may_user_access_osmaxx_frontend(a_user)


def test_superuser_can_access_frontend_even_if_not_in_osmaxx_group(db):
    """
    Superusers cannot be created by anonymous self sign-up, so we don't require explicit group membership for them.
    """
    an_admin = User.objects.create_superuser('A. D. Min', 'admin@example.com', 'password')
    assert _may_user_access_osmaxx_frontend(an_admin)
