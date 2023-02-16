from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from html import unescape as unescape_entities
from django.utils.translation import gettext as _
from furl import furl

RATE_LIMIT_SECONDS = 30


def send_email_confirmation(profile, request, redirection_target):
    user = profile.associated_user
    assert user == request.user
    if cache.get(user.id):
        return
    to_email = profile.unverified_email
    if to_email:
        cache.set(user.id, 'dummy value', timeout=RATE_LIMIT_SECONDS)
        user_administrator_email = settings.OSMAXX['ACCOUNT_MANAGER_EMAIL']
        token = profile.activation_key()
        f = furl(reverse('profile:activation'))
        f.args['token'] = token
        if redirection_target:
            f.args['next'] = redirection_target

        token_url = request.build_absolute_uri(f.url)
        if settings.OSMAXX.get('SECURED_PROXY', False):
            token_url = token_url.replace('http:', 'https:')

        subject = render_to_string(
            'profile/verification_email/subject.txt', context={}
        ).strip()
        subject = ''.join(subject.splitlines())
        subject = unescape_entities(
            subject
        )  # HACK: workaround for https://github.com/geometalab/osmaxx/issues/771
        message = render_to_string(
            'profile/verification_email/body.txt',
            context=dict(
                token_url=token_url,
                username=user.username,
                new_email_address=to_email,
                domain=request.get_host(),
            ),
        )
        message = unescape_entities(
            message
        )  # HACK: workaround for https://github.com/geometalab/osmaxx/issues/771
        send_mail(
            subject=subject,
            message=message,
            from_email=user_administrator_email,
            recipient_list=[to_email],
        )
        messages.add_message(
            request,
            messages.INFO,
            _(
                'To activate your email, click the link in the confirmation email.'
            ),
        )
