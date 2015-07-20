from django.contrib.auth.models import Group
from osmaxx.contrib.auth.frontend_permissions import OSMAXX_FRONTEND_USER


class PermissionHelperMixin(object):
    def add_permissions_to_user(self):
        group = Group.objects.get(name=OSMAXX_FRONTEND_USER)
        self.user.groups.add(group)
