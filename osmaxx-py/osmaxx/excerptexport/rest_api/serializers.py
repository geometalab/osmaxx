from rest_framework_gis import serializers as gis_serializers
from rest_framework_gis.fields import GeometrySerializerMethodField

from osmaxx.excerptexport.models import Excerpt
from osmaxx.excerptexport.models.bounding_geometry import BoundingGeometry


class BoundingGeometrySerializer(gis_serializers.GeoFeatureModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    proxy_for_geometry = GeometrySerializerMethodField()

    def get_proxy_for_geometry(self, obj):
        return obj.subclass_instance.geometry

    class Meta:
        geo_field = 'proxy_for_geometry'
        model = BoundingGeometry
        fields = ['id', 'type_of_geometry']
        auto_bbox = True


class BoundingGeometryFromExcerptSerializer(gis_serializers.GeoFeatureModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    proxy_for_geometry = GeometrySerializerMethodField()

    def get_proxy_for_geometry(self, obj):
        bounding_geometry = obj.bounding_geometry
        return bounding_geometry.subclass_instance.geometry

    class Meta:
        geo_field = 'proxy_for_geometry'
        model = Excerpt
        fields = ['id', 'type_of_geometry']
        auto_bbox = True
