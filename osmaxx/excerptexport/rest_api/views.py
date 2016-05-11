import json

from django.http import HttpResponse
from rest_framework import viewsets

from osmaxx.api_client import ConversionApiClient
from osmaxx.contrib.auth.frontend_permissions import AuthenticatedAndAccessPermission, HasExcerptAccessPermission
from osmaxx.excerptexport.models import Excerpt
from osmaxx.excerptexport.rest_api.serializers import ExcerptGeometrySerializer


class ExcerptViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (
        HasExcerptAccessPermission,
        AuthenticatedAndAccessPermission,
    )
    queryset = Excerpt.objects.all()
    serializer_class = ExcerptGeometrySerializer
excerpt_detail = ExcerptViewSet.as_view({'get': 'retrieve'})


def estimated_file_size(request):
    bbox = {bound: request.GET[bound] for bound in ['north', 'east', 'west', 'south']}
    client = ConversionApiClient()
    response_content = json.dumps(client.estimated_file_size(**bbox))
    return HttpResponse(response_content, content_type="application/json")
