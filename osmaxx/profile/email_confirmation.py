from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.template.defaultfilters import urlencode
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext as _

RATE_LIMIT_SECONDS = 30


def send_email_confirmation(profile, request):
    user = profile.associated_user
    assert user == request.user
    if cache.get(user.id):
        return
    to_email = profile.unverified_email
    if to_email:
        cache.set(user.id, 'dummy value', timeout=RATE_LIMIT_SECONDS)
        user_administrator_email = settings.OSMAXX['ACCOUNT_MANAGER_EMAIL']
        token = profile.activation_key()
        token_url = '{}?token={}'.format(
            request.build_absolute_uri(reverse('profile:activation')), urlencode(token)
        )
        subject = render_to_string('profile/verification_email/subject.txt', context={}).strip()
        subject = ''.join(subject.splitlines())
        message = render_to_string(
            'profile/verification_email/body.txt',
            context=dict(
                token_url=token_url,
                username=user.username,
                new_email_address=to_email,
                domain=request.get_host(),
            )
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=user_administrator_email,
            recipient_list=[to_email],
        )
        messages.add_message(
            request, messages.INFO, _('To activate your email, click the link in the confirmation email.')
        )
