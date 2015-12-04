from django.db import transaction
from rest_framework import serializers
from rest_framework.reverse import reverse

from conversion_job.models import Extent, ConversionJob, GISFormat, GISOption
from converters.converter import Options
from manager.job_manager import ConversionJobManager
from rest_api.serializer_helpers import ModelSideValidationMixin
from shared import JobStatus


class StatusHyperlinkSerializer(serializers.HyperlinkedRelatedField):
    read_only = True
    view_name = 'conversion_job_result-detail'

    def get_url(self, obj, view_name, request, format):   # pragma: nocover
        url = reverse(viewname=self.view_name, kwargs={'rq_job_id': obj.pk}, request=request)
        return url


class ExtentSerializer(ModelSideValidationMixin, serializers.ModelSerializer):
    polyfile = serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)

    class Meta:
        model = Extent
        fields = ('west', 'south', 'east', 'north', 'polyfile')


class GISFormatListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        return data.values_list('format', flat=True)

    def to_internal_value(self, data):
        return super().to_internal_value([{'format': value} for value in data])


class GISFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GISFormat
        fields = ('format',)
        list_serializer_class = GISFormatListSerializer


class GISOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GISOption
        fields = ('coordinate_reference_system', 'detail_level',)


class ConversionJobSerializer(serializers.ModelSerializer):
    extent = ExtentSerializer(many=False)
    gis_formats = GISFormatSerializer(required=False, many=True)
    gis_options = GISOptionSerializer()
    status = StatusHyperlinkSerializer(source='rq_job_id', read_only=True)

    def create(self, validated_data):
        gis_formats = validated_data.pop('gis_formats')
        formats = [d['format'] for d in gis_formats]
        with transaction.atomic():
            validated_data['gis_options_id'] = GISOption.objects.create(**validated_data.pop('gis_options')).id
            extent = Extent.objects.create(**validated_data.pop('extent'))
            validated_data['extent_id'] = extent.id

            ConversionJobModelClass = self.Meta.model  # noqa
            # we need to save, because the path depends on the id!
            conversion_job = ConversionJobModelClass.objects.create(**validated_data)
            rq_job = self._enqueue_rq_job(
                geometry=extent.get_geometry(),
                format_options=Options(output_formats=formats),
                callback_url=validated_data['callback_url'],
                output_directory=conversion_job.output_directory,
            )
            conversion_job.rq_job_id = rq_job.id
            conversion_job.status = JobStatus.QUEUED.technical_representation
            conversion_job.save()
            for gis_format_dict in gis_formats:
                GISFormat.objects.create(conversion_job=conversion_job, **gis_format_dict)
        return conversion_job

    def _enqueue_rq_job(self, geometry, format_options, callback_url, output_directory):
        cm = ConversionJobManager(geometry=geometry, format_options=format_options)
        host = self.context.get('request').get_host()
        return cm.start_conversion(callback_url, output_directory, host)

    class Meta:
        model = ConversionJob
        fields = ('rq_job_id', 'callback_url', 'status', 'gis_formats', 'gis_options', 'extent')
        depth = 1
        read_only_fields = ('rq_job_id', 'status',)


# Status-only serializers

class DownloadURLField(serializers.HyperlinkedRelatedField):
    view_name = 'gisformat-download-result'

    def get_url(self, obj, view_name, request, format):
        gis_format = GISFormat.objects.get(pk=obj.pk)
        if not gis_format.get_result_file_path():
            return None

        url = reverse(viewname=self.view_name, kwargs={'pk': obj.pk}, request=request)
        return url


class GISFormatStatusSerializer(serializers.ModelSerializer):
    progress = serializers.CharField(source='get_progress_display')
    result_url = DownloadURLField(source='pk', read_only=True)

    class Meta:
        model = GISFormat
        fields = ('format', 'progress', 'result_url', )


class ConversionJobStatusSerializer(serializers.ModelSerializer):
    gis_formats = GISFormatStatusSerializer(many=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = ConversionJob
        fields = ('rq_job_id', 'status', 'progress', 'gis_formats')
        read_only_fields = fields
