from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    associated_user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    unverified_email = models.EmailField(_('email'), max_length=200, null=True)
