import json

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework_extensions.etag.mixins import ETAGMixin

from osmaxx.api_client import ConversionApiClient
from osmaxx.contrib.auth.frontend_permissions import AuthenticatedAndAccessPermission, HasExcerptAccessPermission, \
    HasExportAccessPermission
from osmaxx.excerptexport.models import Excerpt, Export
from osmaxx.excerptexport.rest_api.serializers import ExcerptGeometrySerializer, ExportSerializer


class ExcerptViewSet(ETAGMixin, viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (
        HasExcerptAccessPermission,
        AuthenticatedAndAccessPermission,
    )
    queryset = Excerpt.objects.all()
    serializer_class = ExcerptGeometrySerializer
excerpt_detail = ExcerptViewSet.as_view({'get': 'retrieve'})  # noqa: E305 expected 2 blank lines after class or function definition, found 0


class ExportViewSet(viewsets.mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (
        HasExportAccessPermission,
        AuthenticatedAndAccessPermission,
    )
    queryset = Export.objects.all()
    serializer_class = ExportSerializer
export_detail = ExportViewSet.as_view({'delete': 'destroy'})  # noqa: E305 expected 2 blank lines after class or function definition, found 0


def estimated_file_size(request):
    bbox = {bound: request.GET[bound] for bound in ['north', 'east', 'west', 'south']}
    client = ConversionApiClient()
    response_content = json.dumps(client.estimated_file_size(**bbox))
    return HttpResponse(response_content, content_type="application/json")


def format_size_estimation(request):
    client = ConversionApiClient()
    detail_level = request.GET['detail_level']
    estimated_pbf_size = request.GET['estimated_pbf_file_size_in_bytes']
    response_content = json.dumps(
        client.format_size_estimation(detail_level=detail_level, estimated_pbf_size=estimated_pbf_size)
    )
    return HttpResponse(response_content, content_type="application/json")
