from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views import generic

from osmaxx.profile.forms import ProfileForm
from osmaxx.profile.models import Profile


class ProfileView(LoginRequiredMixin, generic.UpdateView):
    form_class = ProfileForm
    template_name = "profile/profile_edit.html"

    def get(self, *args, **kwargs):
        profile = self.get_object()
        user = self.request.user

        if not (user.email or user.profile.unverified_email):
            messages.add_message(
                self.request,
                messages.WARNING,
                _(
                    "You have not set an email address. You must set a valid email address to use OSMaxx."
                ),
            )
        if not profile.has_validated_email():
            messages.add_message(
                self.request,
                messages.WARNING,
                _(
                    "Your email has not been validated. Please check your inbox and validate your email address"
                    " or resend the verification email."
                ),
            )
        if self.is_new_user():
            self._move_email_from_user_to_profile(user, profile)
            profile.request_email_address_confirmation(
                self.request, redirection_target=self.request.GET.get("next")
            )
        else:
            self._ensure_profile_has_email(profile, user)
        user.refresh_from_db()
        return super().get(*args, **kwargs)

    def is_new_user(self):
        user = self.request.user
        profile_is_new = user.profile.unverified_email is None
        user_has_already_access = user_in_frontend_group(user)
        return profile_is_new and not user_has_already_access

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        if isinstance(response, HttpResponseRedirect):  # successful form validation
            profile = Profile.objects.get(associated_user=self.request.user)
            if not profile.has_validated_email():
                profile.request_email_address_confirmation(
                    self.request, redirection_target=self.request.POST.get("next")
                )
        return response

    def _ensure_profile_has_email(self, profile, user):
        if not profile.unverified_email:
            profile.unverified_email = user.email
            profile.save()

    def _move_email_from_user_to_profile(self, user, profile):
        if user.email:
            profile.unverified_email = user.email
            profile.save()
            user.email = ""
            user.save()

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(associated_user=self.request.user)
        return profile

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _("Profile successfully updated")
        )
        return reverse("profile:edit_view")


class ActivationView(LoginRequiredMixin, generic.UpdateView):
    error_msg = _(
        "Verification token too old or invalid. Please resend the confirmation email and try again."
    )

    def get(self, request, *args, **kwargs):
        user = request.user
        token = request.GET.get("token", None)
        if token:
            data = user.profile.validate_key(activation_key=token)
            if data:
                user.email = data["email"]
                user.save()
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    _("Successfully verified your email address."),
                )
                redirection_target = request.GET.get("next", None)
                if redirection_target:
                    return redirect(redirection_target)
            else:
                messages.add_message(self.request, messages.ERROR, self.error_msg)
        else:
            messages.add_message(self.request, messages.ERROR, self.error_msg)
        return redirect(reverse("profile:edit_view"))


class ResendVerificationEmail(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("profile:edit_view")

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(associated_user=self.request.user)
        profile.request_email_address_confirmation(
            self.request, redirection_target=self.request.GET.get("next")
        )
        return super().get(request, *args, **kwargs)


def user_in_frontend_group(user):
    return user.groups.filter(name=settings.OSMAXX_FRONTEND_USER_GROUP).exists()
