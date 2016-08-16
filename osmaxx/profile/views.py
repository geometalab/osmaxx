from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
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
        is_new = not user.groups.filter(name=settings.OSMAXX_FRONTEND_USER_GROUP).exists()

        if is_new:
            self._move_email_from_user_to_profile(user, profile)
        else:
            self._ensure_profile_has_email(profile, user)

        user.refresh_from_db()

        if not user.email or (user.profile.unverified_email != user.email):
            messages.add_message(self.request, messages.INFO, 'Please confirm your email.')
        return super().get(*args, **kwargs)

    def _ensure_profile_has_email(self, profile, user):
        if profile.unverified_email is None:
            profile.unverified_email = user.email
            profile.save()

    def _move_email_from_user_to_profile(self, user, profile):
        if user.email:
            profile.unverified_email = user.email
            profile.save()
            user.email = ''
            user.save()

    def get_object(self, queryset=None):
        return self._get_or_create_profile()

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Profile successfully updated')
        return reverse('profile:edit_view')

    def _get_or_create_profile(self):
        try:
            profile = Profile.objects.get(associated_user=self.request.user)
        except ObjectDoesNotExist:
            profile = Profile.objects.create(associated_user=self.request.user)
        return profile
