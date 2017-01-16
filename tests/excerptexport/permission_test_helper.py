import pytest
from django.conf import settings
from django.contrib.auth.models import Group

from osmaxx.profile.models import Profile


@pytest.mark.django_db
class PermissionHelperMixin(object):
    def add_permissions_to_user(self):
        group = Group.objects.get(name=settings.OSMAXX_FRONTEND_USER_GROUP)
        self.user.groups.add(group)

    def add_email(self):
        self.user.email = 'test@example.com'
        self.user.save()

    def add_valid_email(self):
        self.add_email()
        Profile.objects.get_or_create(associated_user=self.user, unverified_email='test@example.com')
