from rest_framework import serializers

from osmaxx.conversion import output_format
from osmaxx.conversion.converters.converter_gis import detail_levels
from osmaxx.conversion.size_estimator import size_estimation_for_format
from .models import Job, Parametrization


class ParametrizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametrization
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    resulting_file_path = serializers.URLField(source='get_absolute_file_path', read_only=True)

    def save(self, **kwargs):
        request = self.context.get('request', None)
        if request is not None:
            kwargs['own_base_url'] = request.build_absolute_uri('/')
        else:
            kwargs['own_base_url'] = None
        super().save(**kwargs)

    class Meta:
        model = Job
        fields = ['id', 'callback_url', 'parametrization', 'rq_job_id', 'status', 'resulting_file_path',
                  'estimated_pbf_size', 'unzipped_result_size', 'extraction_duration', 'queue_name']
        read_only_fields = ['rq_job_id', 'status', 'resulting_file_path',
                            'estimated_pbf_size', 'unzipped_result_size', 'extraction_duration']


class FormatSizeEstimationSerializer(serializers.Serializer):
    estimated_pbf_file_size_in_bytes = serializers.FloatField()
    detail_level = serializers.ChoiceField(choices=detail_levels.DETAIL_LEVEL_CHOICES)

    def validate(self, data):
        estimated_pbf = data['estimated_pbf_file_size_in_bytes']
        detail_level = data['detail_level']
        data.update(
            {
                output_format: size_estimation_for_format(output_format, detail_level, estimated_pbf)
                for output_format in output_format.DEFINITIONS
            }
        )
        return data

    def to_representation(self, instance):
        return instance
