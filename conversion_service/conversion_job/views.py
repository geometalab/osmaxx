from rest_framework import viewsets, permissions

from conversion_job.models import Extent, ConversionJob
from conversion_job.serializers import ExtentSerializer, ConversionJobSerializer


class ExtentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Extent.objects.all()
    serializer_class = ExtentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class ConversionJobViewSet(viewsets.ModelViewSet):
    queryset = ConversionJob.objects.all()
    serializer_class = ConversionJobSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
