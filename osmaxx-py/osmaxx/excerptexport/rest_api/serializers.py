from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from rest_framework_gis.fields import GeometrySerializerMethodField

from osmaxx.excerptexport.models.bounding_geometry import BoundingGeometry


def get_actual(obj):
    """Expands `obj` to the actual object type.
    """
    for name in dir(obj):
        try:
            attr = getattr(obj, name)
            if isinstance(attr, obj.__class__):
                return attr
        except:
            pass
    return obj


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
        fields = ['id',]
