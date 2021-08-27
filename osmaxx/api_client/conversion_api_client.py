import json
import logging
from osmaxx.conversion.models import Job

from rest_framework import serializers

from osmaxx.conversion.serializers import JobSerializer, ParametrizationSerializer
from osmaxx.clipping_area.serializers import ClippingAreaSerializer

from django.conf import settings
from requests import HTTPError

from osmaxx.api_client.API_client import JWTClient, reasons_for

logger = logging.getLogger(__name__)

SERVICE_BASE_URL = settings.OSMAXX.get("CONVERSION_SERVICE_URL")
LOGIN_URL = "/token-auth/"

USERNAME = settings.OSMAXX.get("CONVERSION_SERVICE_USERNAME")
PASSWORD = settings.OSMAXX.get("CONVERSION_SERVICE_PASSWORD")

CONVERSION_JOB_URL = "/conversion_job/"
ESTIMATED_FILE_SIZE_URL = "/estimate_size_in_bytes/"
FORMAT_SIZE_ESTIMATION_URL = "/format_size_estimation/"


class ConversionApiClient:
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
        job_detail_url = CONVERSION_JOB_URL + "{}/".format(job_id)
        return self.authorized_get(job_detail_url).json()["resulting_file_path"]

    def job_status(self, export):
        assert isinstance(export.conversion_service_job_id, int)
        job = Job.objects.get(pk=export.conversion_service_job_id)
        return job.status

    def estimated_file_size(self, north, west, south, east):
        request_data = {"west": west, "south": south, "east": east, "north": north}
        try:
            response = self.authorized_post(
                ESTIMATED_FILE_SIZE_URL, json_data=request_data
            )
        except HTTPError as e:
            return reasons_for(e)
        return response.json()

    def format_size_estimation(self, estimated_pbf_size, detail_level):
        request_data = {
            "estimated_pbf_file_size_in_bytes": estimated_pbf_size,
            "detail_level": int(detail_level),
        }
        try:
            response = self.authorized_post(
                FORMAT_SIZE_ESTIMATION_URL, json_data=request_data
            )
        except HTTPError as e:
            return reasons_for(e)
        return response.json()


class ResultFileNotAvailableError(RuntimeError):
    pass
