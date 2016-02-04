from rest_framework import permissions, viewsets

from clipping_geometry.models import ClippingArea
from clipping_geometry.serializers import ClippingAreaSerializer


class ClippingAreaViewSet(viewsets.ModelViewSet):
    queryset = ClippingArea.objects.all()
    serializer_class = ClippingAreaSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
