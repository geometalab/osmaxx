from rest_framework import permissions, viewsets

from .models import Job, Parametrization
from .serializers import JobSerializer, ParametrizationSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-id')
    serializer_class = JobSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        super().perform_create(serializer=serializer)
        serializer.instance.start_conversion()


class ParametrizationViewSet(viewsets.ModelViewSet):
    queryset = Parametrization.objects.all()
    serializer_class = ParametrizationSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
