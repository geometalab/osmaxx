from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, viewsets
from django_downloadview.response import DownloadResponse
from rest_framework.decorators import detail_route
from rest_framework.response import Response

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

    @detail_route(methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='download-zip')
    def download_zip(self, request, pk):
        try:
            job = self.queryset.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=404)
        # resulting_file is never falsy, but name (path to the file) is falsy when file is missing on the file-field.
        if not job.resulting_file.name:
            return Response(status=404)
        return DownloadResponse(job.resulting_file, attachment=True)


class ParametrizationViewSet(viewsets.ModelViewSet):
    queryset = Parametrization.objects.all()
    serializer_class = ParametrizationSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
