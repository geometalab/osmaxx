from rest_framework import serializers


class ConverterOptionsSerializer(serializers.Serializer):
    output_formats = serializers.ListField()
