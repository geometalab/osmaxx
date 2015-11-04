from rest_framework import serializers

from conversion_job.models import Extent, ConversionJob, Format
from rest_api.serializer_helpers import ModelSideValidationMixin


class ExtentSerializer(serializers.ModelSerializer, ModelSideValidationMixin):
    polyfile = serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True)

    class Meta:
        model = Extent
        fields = ('id', 'west', 'south', 'east', 'north', 'polyfile')


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ('id', 'progress')


class ConversionJobSerializer(serializers.ModelSerializer):
    formats = FormatSerializer(many=True)
    extent = ExtentSerializer(many=True)

    class Meta:
        model = ConversionJob
        fields = ('id', 'rq_job_id', 'callback_url', 'status', 'formats', 'extent')
        depth = 1
