from rest_framework import generics
from osmaxx.contrib.auth.frontend_permissions import AuthenticatedAndAccessPermission
from osmaxx.excerptexport.models.bounding_geometry import BoundingGeometry
from osmaxx.excerptexport.rest_api.serializers import BoundingGeometrySerializer


class BoundingGeometryMixin:
    serializer_class = BoundingGeometrySerializer
    permission_classes = (AuthenticatedAndAccessPermission,)
    queryset = BoundingGeometry.objects.all()


class BoundingGeometryList(BoundingGeometryMixin, generics.ListAPIView):
    pass


class BoundingGeometryDetail(BoundingGeometryMixin, generics.RetrieveAPIView):
    pass
