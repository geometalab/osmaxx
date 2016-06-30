from rest_framework import serializers

from .models import Job, Parametrization


class ParametrizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametrization


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
                  'estimated_pbf_size', 'unzipped_result_size', 'extraction_duration']
        read_only_fields = ['rq_job_id', 'status', 'resulting_file_path',
                            'estimated_pbf_size', 'unzipped_result_size', 'extraction_duration']
