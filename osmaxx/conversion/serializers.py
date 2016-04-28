from rest_framework import serializers

from .models import Job, Parametrization


class ParametrizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametrization


class JobSerializer(serializers.ModelSerializer):
    resulting_file = serializers.URLField(source='get_download_url', read_only=True)

    def save(self, **kwargs):
        request = self.context.get('request', None)
        if request is not None:
            kwargs['own_base_url'] = request.build_absolute_uri('/')
        else:
            kwargs['own_base_url'] = None
        super().save(**kwargs)

    class Meta:
        model = Job
        fields = ['id', 'callback_url', 'parametrization', 'rq_job_id', 'status', 'resulting_file']
        read_only_fields = ['rq_job_id', 'status', 'resulting_file']
