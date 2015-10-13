from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from rest_framework_gis.fields import GeometrySerializerMethodField

from osmaxx.excerptexport.models.bounding_geometry import BoundingGeometry
from osmaxx.utilities.shortcuts import get_actual


class BoundingGeometrySerializer(serializers.HyperlinkedModelSerializer, gis_serializers.GeoFeatureModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    geom = GeometrySerializerMethodField()

    def get_geom(self, obj):
        actual = get_actual(obj)
        return actual.geometry

    class Meta:
        geo_field = 'geom'
        model = BoundingGeometry
        fields = ['id']
        auto_bbox = True
