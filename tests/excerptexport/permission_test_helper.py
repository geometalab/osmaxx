import pytest
from django.conf import settings
from django.contrib.auth.models import Group


@pytest.mark.django_db
class PermissionHelperMixin(object):
    def add_permissions_to_user(self):
        group = Group.objects.get(name=settings.OSMAXX_FRONTEND_USER_GROUP)
        self.user.groups.add(group)
