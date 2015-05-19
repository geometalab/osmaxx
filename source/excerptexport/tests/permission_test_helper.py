from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from excerptexport.models import Excerpt, ExtractionOrder
from excerptexport.models.bounding_geometry import BoundingGeometry


class PermissionHelperMixin(object):
    @staticmethod
    def _permission_for(model, codename):
        content_type = ContentType.objects.get_for_model(model)
        permission = Permission.objects.get(content_type=content_type, codename=codename)
        return permission

    def add_permissions_to_user(self):
        self.user.user_permissions.add(self._permission_for(BoundingGeometry, 'add_boundinggeometry'))
        self.user.user_permissions.add(self._permission_for(BoundingGeometry, 'change_boundinggeometry'))
        self.user.user_permissions.add(self._permission_for(Excerpt, 'add_excerpt'))
        self.user.user_permissions.add(self._permission_for(Excerpt, 'change_excerpt'))
        self.user.user_permissions.add(self._permission_for(ExtractionOrder, 'add_extractionorder'))
        self.user.user_permissions.add(self._permission_for(ExtractionOrder, 'change_extractionorder'))
