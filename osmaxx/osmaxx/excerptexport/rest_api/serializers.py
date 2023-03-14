from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from rest_framework_gis.fields import GeometrySerializerMethodField

from osmaxx.excerptexport.models import Excerpt, Export


class ExcerptGeometrySerializer(gis_serializers.GeoFeatureModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    geometry = GeometrySerializerMethodField()

    def get_geometry(self, obj):
        return obj.geometry

    class Meta:
        geo_field = 'geometry'
        model = Excerpt
        fields = ['id', 'excerpt_type', 'color']
        auto_bbox = True


class ExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Export
        fields = ['id', 'status']
