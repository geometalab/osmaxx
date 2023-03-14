import pytest

from osmaxx.profile.models import Profile


@pytest.mark.django_db
class PermissionHelperMixin(object):
    def add_email(self):
        self.user.email = 'test@example.com'
        self.user.save()

    def add_valid_email(self):
        self.add_email()
        Profile.objects.get_or_create(associated_user=self.user, unverified_email='test@example.com')
