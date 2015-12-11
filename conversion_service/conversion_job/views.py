import os

from django.http import FileResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from conversion_job.models import Extent, ConversionJob, GISFormat
from conversion_job.serializers import ExtentSerializer, ConversionJobSerializer, ConversionJobStatusSerializer, \
    GISFormatStatusSerializer


class ExtentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Extent.objects.all()
    serializer_class = ExtentSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )


class ConversionJobViewSet(viewsets.ModelViewSet):
    queryset = ConversionJob.objects.all()
    serializer_class = ConversionJobSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )


class ConversionJobStatusViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'rq_job_id'
    lookup_value_regex = '[0-9a-f-]{36}'

    queryset = ConversionJob.objects.all()
    serializer_class = ConversionJobStatusSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def retrieve(self, request, *args, **kwargs):
        # update conversion status
        self.get_object().update_status_from_rq()
        return super().retrieve(request, *args, **kwargs)


class GISFormatStatusViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GISFormat.objects.all()
    serializer_class = GISFormatStatusSerializer

    @detail_route()
    def download_result(self, *args, **kwargs):
        file_path = self.get_object().get_result_file_path()
        file_name = file_path.split('/')[-1]
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        return response

    @detail_route(methods=['delete'])
    def delete_result(self, *args, **kwargs):
        format_obj = self.get_object()
        file_path = format_obj.get_result_file_path()
        # ignore when file isn't there
        if file_path:
            os.remove(format_obj.get_result_file_path())
        return Response(status=status.HTTP_204_NO_CONTENT)
