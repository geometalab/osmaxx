import pytest
from django.contrib.auth.models import User
from osmaxx.contrib.auth.frontend_permissions import _user_has_validated_email
from osmaxx.profile.models import Profile


def test_new_user_has_no_validated_email_address(db):
    a_user = User.objects.create_user('U. Ser', 'user@example.com', 'password')
    assert not _user_has_validated_email(a_user)


def test_user_with_same_address_on_profile_has_validated_email_address(db):
    a_user = User.objects.create_user('U. Ser', 'user@example.com', 'password')
    Profile.objects.create(associated_user=a_user, unverified_email=a_user.email)
    assert _user_has_validated_email(a_user)


def test_new_superuser_has_no_validated_email_address(db):
    an_admin = User.objects.create_superuser('A. D. Min', 'admin@example.com', 'password')
    assert not _user_has_validated_email(an_admin)


@pytest.mark.parametrize('user_email', ['', None])
@pytest.mark.parametrize('profile_email', ['', None])
def test_user_with_empty_email_addresses(db, user_email, profile_email):
    a_user = User.objects.create_user('U. Ser', user_email, 'password')
    Profile.objects.create(associated_user=a_user, unverified_email=profile_email)
    assert not _user_has_validated_email(a_user)
