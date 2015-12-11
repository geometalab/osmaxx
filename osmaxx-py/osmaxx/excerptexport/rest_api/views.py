import json
from django.db import models
from rest_framework import generics
from django.http import HttpResponse
from osmaxx.contrib.auth.frontend_permissions import AuthenticatedAndAccessPermission, HasBBoxAccessPermission, \
    HasExcerptAccessPermission

from osmaxx.excerptexport.models import Excerpt
from osmaxx.excerptexport.models.bounding_geometry import BoundingGeometry
from osmaxx.excerptexport.rest_api.serializers import BoundingGeometrySerializer, BoundingGeometryFromExcerptSerializer
from osmaxx.excerptexport.services.shortcuts import get_authenticated_api_client


class BoundingGeometryMixin:
    serializer_class = BoundingGeometrySerializer
    permission_classes = (AuthenticatedAndAccessPermission, HasBBoxAccessPermission,)
    queryset = BoundingGeometry.objects.all()


class BoundingGeometryList(BoundingGeometryMixin, generics.ListAPIView):
    def get_queryset(self):
        return self.queryset.filter(models.Q(excerpt__owner=self.request.user) | models.Q(excerpt__is_public=True))


class BoundingGeometryDetail(BoundingGeometryMixin, generics.RetrieveAPIView):
    pass


class BoundingGeometryFromExcerptMixin:
    serializer_class = BoundingGeometryFromExcerptSerializer
    permission_classes = (AuthenticatedAndAccessPermission, HasExcerptAccessPermission,)
    queryset = Excerpt.objects.all()


class BoundingGeometryFromExcerptList(BoundingGeometryFromExcerptMixin, generics.ListAPIView):
    def get_queryset(self):
        return self.queryset.filter(models.Q(owner=self.request.user) | models.Q(is_public=True))


class BoundingGeometryFromExcerptDetail(BoundingGeometryFromExcerptMixin, generics.RetrieveAPIView):
    pass


def estimated_file_size(request):
    file_size_estimation = get_authenticated_api_client().estimated_file_size(
        north=request.GET['north'], east=request.GET['east'], west=request.GET['west'], south=request.GET['south']
    )
    return HttpResponse(json.dumps(file_size_estimation), content_type="application/json")


def country_geojson(request, pk):
    client = get_authenticated_api_client()
    country_json_from_conversion_service = client.get_country_geojson(pk)

    return HttpResponse(
        country_json_from_conversion_service,
        content_type="application/json"
    )
