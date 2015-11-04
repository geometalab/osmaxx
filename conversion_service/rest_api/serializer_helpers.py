from django.core.exceptions import ValidationError
from rest_framework import serializers


class ModelSideValidationMixin(object):
    def is_valid(self, *args, **kwargs):
        is_valid = super().is_valid(*args, **kwargs)
        try:
            self.Meta.model(**self.validated_data).clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message)
        return is_valid
