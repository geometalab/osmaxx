from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ViewSet

from osmaxx.geodesy.serializers import UTMZoneSerializer


class UTMZonesForGeometryViewSet(ViewSet):
    """
    Retrieve valid UTM-Zones for a given geometry on world coordinates.
    """
    serializer_class = UTMZoneSerializer
    permission_classes = (
        (permissions.IsAuthenticated,)
    )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}
