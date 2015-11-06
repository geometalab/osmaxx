from django.db import transaction
from rest_framework import serializers

from conversion_job.models import Extent, ConversionJob, GISFormat, GISOption
from converters.converter import Options
from manager.job_manager import ConversionJobManager
from rest_api.serializer_helpers import ModelSideValidationMixin
from shared import JobStatus


class ExtentSerializer(ModelSideValidationMixin, serializers.ModelSerializer):
    polyfile = serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True)

    class Meta:
        model = Extent
        fields = ('id', 'west', 'south', 'east', 'north', 'polyfile')


class GISFormatListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        formats = [GISFormat(**item) for item in validated_data]
        return GISFormat.objects.bulk_create(formats)

    def to_representation(self, data):
        return data.values_list('format', flat=True)

    def to_internal_value(self, data):
        """
        List of strings to list of dicts of native values <- List of dicts of primitive datatypes.
        """
        ret = []
        for value in data:
            ret.append({'format': value})
        return super().to_internal_value(ret)


class GISFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GISFormat
        fields = ('format',)
        list_serializer_class = GISFormatListSerializer


class GISOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GISOption
        fields = ('crs', 'detail_level',)


class ConversionJobSerializer(serializers.ModelSerializer):
    extent = ExtentSerializer(many=False)
    gis_formats = GISFormatSerializer(required=False, many=True)
    gis_option = GISOptionSerializer()

    def create(self, validated_data):
        gis_formats = validated_data.pop('gis_formats')
        with transaction.atomic():
            gis_option = GISOption(**validated_data.pop('gis_option'))
            gis_option.save()
            validated_data['gis_option'] = gis_option
            extent = Extent(**validated_data.pop('extent'))
            extent.save()
            validated_data['extent'] = extent
            conversion_job = super().create(validated_data)
            formats = []
            for gis_format_dict in gis_formats:
                formats.append(gis_format_dict['format'])
                gis_format_dict['conversion_job'] = conversion_job
                gis_format = GISFormat(**gis_format_dict)
                gis_format.save()
            rq_job = self._enqueue_rq_job(
                geometry=extent.get_geometry(),
                format_options=Options(output_formats=formats),
                callback_url=conversion_job.callback_url,
                output_directory=conversion_job.output_directory,
            )
            conversion_job.rq_job_id = rq_job.id
            conversion_job.status = JobStatus.QUEUED.value
            conversion_job.save()
        return conversion_job

    def _enqueue_rq_job(self, geometry, format_options, callback_url, output_directory):
        cm = ConversionJobManager(geometry=geometry, format_options=format_options)
        return cm.start_conversion(callback_url, output_directory)

    class Meta:
        model = ConversionJob
        fields = ('id', 'rq_job_id', 'callback_url', 'status', 'gis_formats', 'gis_option', 'extent')
        depth = 1
        read_only_fields = ('rq_job_id', 'status',)


# Status Only Serializers

class GISFormatStatusSerializer(serializers.ModelSerializer):
    progress = serializers.CharField(source='get_progress_display')

    class Meta:
        model = GISFormat
        fields = ('format', 'progress',)


class ConversionJobStatusSerializer(serializers.ModelSerializer):
    gis_formats = GISFormatStatusSerializer(many=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = ConversionJob
        fields = ('rq_job_id', 'status', 'progress', 'gis_formats')
        read_only_fields = fields
