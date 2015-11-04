from rest_framework import viewsets
from rest_framework.response import Response

from converters import converter_options
from rest_api.serializers import ConverterOptionsSerializer


class FormatOptionsViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing format options.
    """

    def list(self, request):
        serializer = ConverterOptionsSerializer(converter_options)
        return Response(serializer.data)
