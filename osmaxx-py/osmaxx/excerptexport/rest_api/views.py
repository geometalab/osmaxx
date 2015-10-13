from django.db import models
from rest_framework import generics
from osmaxx.contrib.auth.frontend_permissions import AuthenticatedAndAccessPermission, HasBBoxAccessPermission
from osmaxx.excerptexport.models.bounding_geometry import BoundingGeometry
from osmaxx.excerptexport.rest_api.serializers import BoundingGeometrySerializer


class BoundingGeometryMixin:
    serializer_class = BoundingGeometrySerializer
    permission_classes = (AuthenticatedAndAccessPermission, HasBBoxAccessPermission,)
    queryset = BoundingGeometry.objects.all()


class BoundingGeometryList(BoundingGeometryMixin, generics.ListAPIView):
    def get_queryset(self):
        return self.queryset.filter(models.Q(excerpt__owner=self.request.user) | models.Q(excerpt__is_public=True))


class BoundingGeometryDetail(BoundingGeometryMixin, generics.RetrieveAPIView):
    pass
