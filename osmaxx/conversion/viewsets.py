from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .serializers import FormatSizeEstimationSerializer


class FormatSizeEstimationView(viewsets.ViewSet):
    """
    Returns the estimated file size for osm data of the given extent
    """

    serializer_class = FormatSizeEstimationSerializer

    def get_success_headers(self, data):
        try:
            return {"Location": data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)
