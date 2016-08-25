from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from osmaxx.conversion_api.coordinate_reference_systems import WGS_84
from osmaxx.geodesy.coordinate_reference_system import utm_zones_for_representing


class UTMZoneSerializer(serializers.Serializer):
    geometry = gis_serializers.GeometryField(allow_null=False, required=True)
    utm_zones = serializers.ListField(read_only=True)

    def to_representation(self, instance):
        if hasattr(instance['geometry'], 'srid') or instance['geometry'].srid is None:
            instance['geometry'].srid = WGS_84
        representation = super().to_representation(instance=instance)
        representation['utm_zones'] = [
            dict(srid=zone.srid, name=str(zone))
            for zone in utm_zones_for_representing(instance['geometry'])
        ]
        return representation

    def create(self, validated_data, *args, **kwargs):
        return dict(utm_zones=utm_zones_for_representing(validated_data['geometry']))

    def save(self, **kwargs):  # small hack to still be able to use the default serializer
        pass
