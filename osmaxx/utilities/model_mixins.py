from django.core.urlresolvers import reverse
from django.db import models


class AdminUrlModelMixin(models.Model):
    class Meta:
        abstract = True

    def get_admin_url(self):
        admin_view_name = 'admin:{app_label}_{model_name}_change'.format(
            app_label=self._meta.app_label,
            model_name=self._meta.model_name,
        )
        return reverse(admin_view_name, args=(self.id,))
