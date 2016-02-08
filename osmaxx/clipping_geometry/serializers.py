from django.contrib.gis import geos
from django.utils.translation import gettext as _
from rest_framework import serializers

from .models import ClippingArea


class ClippingAreaSerializer(serializers.ModelSerializer):
    def validate_clipping_multi_polygon(self, clipping_multi_polygon):
        if type(clipping_multi_polygon) != geos.MultiPolygon:
            raise serializers.ValidationError(
                _(
                    "The received geometry is not a MultiPolygon. Received type of {other_type}.".format(
                        other_type=clipping_multi_polygon.__class__.__name__
                    )
                )
            )
        # prevent obscure IntegrityError in the database:
        # occurs for example when the geoJSON seems valid, but contains non-coordinate string(s).
        if clipping_multi_polygon.num_coords <= 0:
            raise serializers.ValidationError(
                _("Invalid coordinates: expected at least one coordinate pair, received none.")
            )
        return clipping_multi_polygon

    class Meta:
        model = ClippingArea
        geo_field = "clipping_multi_polygon"
        fields = ['id', 'name', 'clipping_multi_polygon']
