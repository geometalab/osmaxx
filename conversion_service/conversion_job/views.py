import django_rq
from django.http import FileResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import detail_route

from conversion_job.models import Extent, ConversionJob, GISFormat
from conversion_job.serializers import ExtentSerializer, ConversionJobSerializer, ConversionJobStatusSerializer, \
    GISFormatStatusSerializer
from shared import rq_job_status_mapping, ConversionProgress, JobStatus


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


class ConversionJobStatusViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'rq_job_id'
    lookup_value_regex = '[0-9a-f-]{36}'

    queryset = ConversionJob.objects.all()
    serializer_class = ConversionJobStatusSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def retrieve(self, request, *args, **kwargs):
        self._update_status_from_rq()
        return super().retrieve(request, *args, **kwargs)

    def _update_status_from_rq(self):
        conversion_job = self.get_object()
        rq_job = django_rq.get_queue().fetch_job(job_id=conversion_job.rq_job_id)

        # only do work if the job is not yet deleted
        if rq_job:
            # don't set the status if we're already done
            if conversion_job.status != JobStatus.DONE.value:
                conversion_job.status = rq_job_status_mapping[rq_job.status].value

            progress = rq_job.meta.get('progress', None)
            if progress:
                progress_state = progress.value
                for gis_format in conversion_job.gis_formats.all():
                    if gis_format.progress != ConversionProgress.SUCCESSFUL.value:
                        gis_format.progress = progress_state
                        gis_format.save()
            conversion_job.save()


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
