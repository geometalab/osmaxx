from rest_framework import serializers

from osmaxx.conversion import output_format
from osmaxx.conversion.converters.converter_gis import detail_levels
from osmaxx.conversion.size_estimator import size_estimation_for_format


class FormatSizeEstimationSerializer(serializers.Serializer):
    estimated_pbf_file_size_in_bytes = serializers.FloatField()
    detail_level = serializers.ChoiceField(choices=detail_levels.DETAIL_LEVEL_CHOICES)

    def validate(self, data):
        estimated_pbf = data["estimated_pbf_file_size_in_bytes"]
        detail_level = data["detail_level"]
        data.update(
            {
                output_format: size_estimation_for_format(
                    output_format, detail_level, estimated_pbf
                )
                for output_format in output_format.DEFINITIONS
            }
        )
        return data

    def to_representation(self, instance):
        return instance
