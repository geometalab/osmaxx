from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Country


class CountrySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Country
        geo_field = 'simplified_polygon'
        fields = (
            'id',
            'name',
            'simplified_polygon',
            'type_of_geometry',
        )
