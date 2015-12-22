from django.conf import settings

from rest_framework import serializers

from file_size_estimation.estimate_size import estimate_size_of_extent

csv_source_file = settings.OSMAXX_CONVERSION_SERVICE['ESTIMATION_CSV_SOURCE_FILE']


class FileEstimationSerializer(serializers.Serializer):
    west = serializers.FloatField()
    south = serializers.FloatField()
    east = serializers.FloatField()
    north = serializers.FloatField()

    def validate(self, data):
        data.update({
            'estimated_file_size_in_bytes': estimate_size_of_extent(
                csv_source_file,
                west=data['west'],
                south=data['south'],
                east=data['east'],
                north=data['north'],
            )
        })
        return data

    def to_representation(self, instance):
        return instance
