from datetime import timedelta

from django.conf import settings
from django.core import signing
from django.db import models
from django.utils.translation import ugettext_lazy as _

PROFILE_SALT = 'profile'


class Profile(models.Model):
    associated_user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    unverified_email = models.EmailField(verbose_name=_('unverified email'), max_length=200, null=True)

    def activation_key(self):
        key = signing.dumps(
            obj=self._username_email_dict(),
            salt=PROFILE_SALT)
        return key

    def validate_key(self, activation_key):
        try:
            return signing.loads(
                activation_key,
                salt=PROFILE_SALT,
                max_age=timedelta(days=settings.REGISTRATION_VERIFICATION_TIMEOUT_DAYS)
            )
        except signing.BadSignature:
            return None

    def _username_email_dict(self):
        return {'username': self.associated_user.username, 'email': self.unverified_email}
