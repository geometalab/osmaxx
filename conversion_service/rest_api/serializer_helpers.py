from django.core.exceptions import ValidationError
from rest_framework import serializers


class ModelSideValidationMixin(object):
    def validate(self, data):
        try:
            self.Meta.model(**data).clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message)
        return super().validate(data)
