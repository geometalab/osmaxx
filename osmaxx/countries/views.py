from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .models import Country
from .serializers import CountrySerializer, CountryListSerializer


class CountryViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def list(self, request, *args, **kwargs):
        serializer = CountryListSerializer(self.queryset, many=True)
        return Response(serializer.data)
