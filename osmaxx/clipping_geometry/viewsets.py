from rest_framework import permissions, viewsets

from .models import ClippingArea
from .serializers import ClippingAreaSerializer


class ClippingAreaViewSet(viewsets.ModelViewSet):
    queryset = ClippingArea.objects.all()
    serializer_class = ClippingAreaSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
