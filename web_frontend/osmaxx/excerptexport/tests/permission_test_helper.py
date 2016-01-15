from django.contrib.auth.models import Group
from osmaxx.contrib.auth.frontend_permissions import FRONTEND_USER_GROUP


class PermissionHelperMixin(object):
    def add_permissions_to_user(self):
        group = Group.objects.get(name=FRONTEND_USER_GROUP)
        self.user.groups.add(group)
