from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.defaultfilters import urlencode
from django.utils.translation import ugettext as _
from django.views import generic

from osmaxx.contrib.auth.frontend_permissions import LoginRequiredMixin
from osmaxx.profile.forms import ProfileForm
from osmaxx.profile.models import Profile


class ProfileView(LoginRequiredMixin, generic.UpdateView):
    form_class = ProfileForm
    template_name = 'profile/profile_edit.html'

    def get(self, *args, **kwargs):
        profile = self._get_or_create_profile()
        user = self.request.user
        if not (user.email or user.profile.unverified_email):
            messages.add_message(
                self.request,
                messages.WARNING,
                _('You have not set an email. You must set a valid email to use OSMaxx.')
            )
        if self.is_new_user():
            self._move_email_from_user_to_profile(user, profile)
            self._send_email_verification(profile)
        else:
            self._ensure_profile_has_email(profile, user)
        user.refresh_from_db()
        return super().get(*args, **kwargs)

    def is_new_user(self):
        user = self.request.user
        return not (
            user.profile.unverified_email or user.groups.filter(name=settings.OSMAXX_FRONTEND_USER_GROUP).exists()
        )

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        if isinstance(response, HttpResponseRedirect):  # successful form validation
            self._send_email_verification(profile=Profile.objects.get(associated_user=self.request.user))
        return response

    def _ensure_profile_has_email(self, profile, user):
        if profile.unverified_email in (None, ''):
            profile.unverified_email = user.email
            profile.save()

    def _move_email_from_user_to_profile(self, user, profile):
        if user.email:
            profile.unverified_email = user.email
            profile.save()
            user.email = ''
            user.save()

    def _send_email_verification(self, profile):
        to_email = profile.unverified_email
        if to_email:
            user_administrator_email = settings.OSMAXX['ACCOUNT_MANAGER_EMAIL']
            token = profile.activation_key()
            subject = _('Verify your email address')
            message = _('In order to verify your email-address click the following link:\n'
                        '{}?token={}'
                        '\n'
                        'If it wasn\'t you, just ignore this email.\n'
                        .format(self.request.build_absolute_uri(reverse('profile:activation')), urlencode(token)))
            send_mail(
                subject=subject,
                message=message,
                from_email=user_administrator_email,
                recipient_list=[to_email],
            )
            messages.add_message(
                self.request, messages.INFO, _('To activate your email, click the link in the confirmation email.')
            )

    def get_object(self, queryset=None):
        return self._get_or_create_profile()

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, _('Profile successfully updated'))
        return reverse('profile:edit_view')

    def _get_or_create_profile(self):
        try:
            profile = Profile.objects.get(associated_user=self.request.user)
        except ObjectDoesNotExist:
            profile = Profile.objects.create(associated_user=self.request.user)
        return profile


class ActivationView(LoginRequiredMixin, generic.UpdateView):
    error_msg = _('Verification token too old or invalid. Please resend the verification email and try again.')

    def get(self, request, *args, **kwargs):
        user = request.user
        token = request.GET.get('token', None)
        if token:
            data = user.profile.validate_key(activation_key=token)
            if data:
                user.email = data['email']
                user.save()
                self._set_group(user)
                messages.add_message(self.request, messages.SUCCESS, _('Successfully verified your email.'))
            else:
                messages.add_message(self.request, messages.ERROR, self.error_msg)
        else:
            messages.add_message(self.request, messages.ERROR, self.error_msg)
        return redirect(reverse('profile:edit_view'))

    def _set_group(self, user):
        if settings.REGISTRATION_OPEN and not self._user_in_frontend_group(user):
            self._grant_user_access(user)
        if self._user_in_frontend_group(user):
            messages.add_message(self.request, messages.SUCCESS,
                                 _('Your email address is now active.'))

    def _user_in_frontend_group(self, user):
        return user.groups.filter(name=settings.OSMAXX_FRONTEND_USER_GROUP).exists()

    def _grant_user_access(self, user):
        group = Group.objects.get(name=settings.OSMAXX_FRONTEND_USER_GROUP)
        group.user_set.add(user)


class ResendVerificationEmail(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('profile:edit_view')

    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)
