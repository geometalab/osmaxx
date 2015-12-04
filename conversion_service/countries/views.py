from rest_framework import viewsets, permissions

from countries.models import Country
from countries.serializers import CountrySerializer


class CountryViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
