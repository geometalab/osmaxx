from rest_framework import serializers

from conversion_job.models import Extent, ConversionJob, FormatOption
from manager.job_manager import ConversionJobManager
from rest_api.serializer_helpers import ModelSideValidationMixin


class ExtentSerializer(serializers.ModelSerializer, ModelSideValidationMixin):
    polyfile = serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True)

    class Meta:
        model = Extent
        fields = ('id', 'west', 'south', 'east', 'north', 'polyfile')


class FormatOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormatOption
        fields = ('id', 'progress')


class ConversionJobSerializer(serializers.ModelSerializer):
    format_options = FormatOptionSerializer(many=True)
    extent = ExtentSerializer(many=True)

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.rq_job_id = self._enqueue_rq_job(
            instance.extent.get_geometry(),
            instance.get_format_options(),
            instance.callback_url,
        )

    def _enqueue_rq_job(self, geometry, format_options, callback_url):
        cm = ConversionJobManager(geometry=geometry, format_options=format_options)
        return cm.start_conversion(callback_url)

    class Meta:
        model = ConversionJob
        fields = ('id', 'rq_job_id', 'callback_url', 'status', 'format_options', 'extent')
        depth = 1
        read_only_fields = ('rq_job_id', 'status',)
