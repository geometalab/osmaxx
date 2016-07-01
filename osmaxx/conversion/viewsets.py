from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .models import Job, Parametrization
from .serializers import JobSerializer, ParametrizationSerializer, FormatSizeEstimationSerializer


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


class FormatSizeEstimationView(viewsets.ViewSet):
    """
    Returns the estimated file size for osm data of the given extent
    """
    serializer_class = FormatSizeEstimationSerializer

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)
