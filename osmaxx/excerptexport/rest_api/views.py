import json
from osmaxx.conversion import output_format
from osmaxx.conversion.size_estimator import size_estimation_for_format

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework_extensions.etag.mixins import ETAGMixin

from pbf_file_size_estimation.estimate_size import estimate_size_of_extent
from osmaxx.contrib.auth.frontend_permissions import (
    AuthenticatedAndAccessPermission,
    HasExcerptAccessPermission,
    HasExportAccessPermission,
)
from osmaxx.excerptexport.models import Excerpt, Export
from osmaxx.excerptexport.rest_api.serializers import (
    ExcerptGeometrySerializer,
    ExportSerializer,
)


class ExcerptViewSet(
    ETAGMixin, viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    permission_classes = (
        HasExcerptAccessPermission,
        AuthenticatedAndAccessPermission,
    )
    queryset = Excerpt.objects.all()
    serializer_class = ExcerptGeometrySerializer


excerpt_detail = ExcerptViewSet.as_view(
    {"get": "retrieve"}
)


class ExportViewSet(viewsets.mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (
        HasExportAccessPermission,
        AuthenticatedAndAccessPermission,
    )
    queryset = Export.objects.all()
    serializer_class = ExportSerializer


export_detail = ExportViewSet.as_view(
    {"delete": "destroy"}
)


def estimated_file_size(request):
    from pbf_file_size_estimation.app_settings import (
        PBF_FILE_SIZE_ESTIMATION_CSV_FILE_PATH,
    )

    size_csv = PBF_FILE_SIZE_ESTIMATION_CSV_FILE_PATH
    bbox = {
        bound: float(request.GET[bound]) for bound in ["north", "east", "west", "south"]
    }
    size = estimate_size_of_extent(
        size_csv,
        west=bbox["west"],
        south=bbox["south"],
        east=bbox["east"],
        north=bbox["north"],
    )
    response_content = json.dumps({"estimated_file_size_in_bytes": size})
    return HttpResponse(response_content, content_type="application/json")


def format_size_estimation(request):
    detail_level = int(request.GET["detail_level"])
    estimated_pbf_size = float(request.GET["estimated_pbf_file_size_in_bytes"])
    result = {
        format_name: size_estimation_for_format(
            format_name, detail_level, estimated_pbf_size
        )
        for format_name in output_format.DEFINITIONS
    }
    response_content = json.dumps(result)
    return HttpResponse(response_content, content_type="application/json")
