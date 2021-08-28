import json
import logging
from osmaxx.conversion.models import Job

from rest_framework import serializers

from osmaxx.conversion.serializers import JobSerializer, ParametrizationSerializer
from osmaxx.clipping_area.serializers import ClippingAreaSerializer

from django.conf import settings


logger = logging.getLogger(__name__)

CONVERSION_JOB_URL = "/conversion_job/"


class ConversionJobHelper:
    def create_boundary(self, multipolygon, *, name):
        geo_json = json.loads(multipolygon.json)
        json_payload = dict(name=name, clipping_multi_polygon=geo_json)
        serializer = ClippingAreaSerializer(data=json_payload)
        serializer.is_valid()
        clipping_area = serializer.save()
        return clipping_area

    def create_parametrization(
        self,
        *,
        clipping_area,
        out_format,
        detail_level,
        out_srs,
    ):
        data = dict(
            clipping_area=clipping_area.id,
            out_format=out_format,
            detail_level=detail_level,
            out_srs=out_srs,
        )
        serializer = ParametrizationSerializer(data=data)
        serializer.is_valid()
        paramatrization = serializer.save()
        return paramatrization

    def create_job(self, parametrization, user, request):
        data = dict(
            parametrization=parametrization.id,
            queue_name=self._priority_queue_name(user),
        )
        serializer = JobSerializer(data=data, context={"request": request})

        if serializer.is_valid():
            job = serializer.save()
            return job
        print(serializer.error)
        raise serializers.ValidationError(serializer.error)

    def get_result_file_path(self, job_id):
        file_path = self._get_result_file_path(job_id)
        if file_path:
            return file_path
        raise ResultFileNotAvailableError

    def _priority_queue_name(self, user):
        if user.groups.filter(name=settings.OSMAXX["EXCLUSIVE_USER_GROUP"]).exists():
            return "high"
        return "default"

    def _get_result_file_path(self, job_id):
        # TODO: return file path
        return f"file_path if {id}"

    def job_status(self, export):
        assert isinstance(export.conversion_service_job_id, int)
        job = Job.objects.get(pk=export.conversion_service_job_id)
        return job.status


class ResultFileNotAvailableError(RuntimeError):
    pass
