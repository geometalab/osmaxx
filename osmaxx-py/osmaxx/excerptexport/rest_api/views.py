from django.db import models
from rest_framework import generics
from osmaxx.contrib.auth.frontend_permissions import AuthenticatedAndAccessPermission, HasBBoxAccessPermission, \
    HasExcerptAccessPermission
from osmaxx.excerptexport.models import Excerpt
from osmaxx.excerptexport.models.bounding_geometry import BoundingGeometry
from osmaxx.excerptexport.rest_api.serializers import BoundingGeometrySerializer, BoundingGeometryFromExcerptSerializer


class BoundingGeometryMixin:
    serializer_class = BoundingGeometrySerializer
    permission_classes = (AuthenticatedAndAccessPermission, HasBBoxAccessPermission,)
    queryset = BoundingGeometry.objects.all()


class BoundingGeometryList(BoundingGeometryMixin, generics.ListAPIView):
    def get_queryset(self):
        return self.queryset.filter(models.Q(excerpt__owner=self.request.user) | models.Q(excerpt__is_public=True))


class BoundingGeometryDetail(BoundingGeometryMixin, generics.RetrieveAPIView):
    pass


class BoundingGeometryFromExcerptMixin:
    serializer_class = BoundingGeometryFromExcerptSerializer
    permission_classes = (AuthenticatedAndAccessPermission, HasExcerptAccessPermission,)
    queryset = Excerpt.objects.all()


class BoundingGeometryFromExcerptList(BoundingGeometryFromExcerptMixin, generics.ListAPIView):
    def get_queryset(self):
        return self.queryset.filter(models.Q(owner=self.request.user) | models.Q(is_public=True))


class BoundingGeometryFromExcerptDetail(BoundingGeometryFromExcerptMixin, generics.RetrieveAPIView):
    pass
