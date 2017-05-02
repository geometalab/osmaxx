from datetime import timedelta

from django.conf import settings
from django.core import signing
from django.db import models
from django.utils.translation import ugettext_lazy as _

from osmaxx.profile.email_confirmation import send_email_confirmation


class Profile(models.Model):
    REGISTRATION_VERIFICATION_TIMEOUT_DAYS = 2
    PROFILE_SALT = 'profile'

    associated_user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE)
    unverified_email = models.EmailField(verbose_name=_('unverified email'), max_length=200, null=True)

    def has_validated_email(self):
        return self.unverified_email and self.associated_user.email == self.unverified_email

    def activation_key(self):
        key = signing.dumps(
            obj=self._username_email_dict(),
            salt=self.PROFILE_SALT)
        return key

    def request_email_address_confirmation(self, request):
        send_email_confirmation(profile=self, request=request)

    def validate_key(self, activation_key):
        try:
            return signing.loads(
                activation_key,
                salt=self.PROFILE_SALT,
                max_age=timedelta(days=self.REGISTRATION_VERIFICATION_TIMEOUT_DAYS)
            )
        except signing.BadSignature:
            return None

    def _username_email_dict(self):
        return {'username': self.associated_user.username, 'email': self.unverified_email}
