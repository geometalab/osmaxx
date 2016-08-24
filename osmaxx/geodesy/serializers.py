from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from osmaxx.geodesy.coordinate_reference_system import utm_zones_for_representing


class UTMZoneSerializer(serializers.Serializer):
    geometry = gis_serializers.GeometryField(allow_null=False, required=True)
    utm_zones = serializers.ListField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)
        representation['utm_zones'] = [str(zone) for zone in utm_zones_for_representing(instance['geometry'])]
        return representation

    def create(self, validated_data, *args, **kwargs):
        return dict(utm_zones=utm_zones_for_representing(validated_data['geometry']))

    def save(self, **kwargs):  # small hack to still be able to use the default serializer
        pass
