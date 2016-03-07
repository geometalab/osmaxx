from rest_framework import viewsets, permissions

from .models import Country
from .serializers import CountrySerializer


class CountryViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
country_detail = CountryViewSet.as_view({'get': 'retrieve'})
