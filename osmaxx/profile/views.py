from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.views import generic

from osmaxx.contrib.auth.frontend_permissions import LoginRequiredMixin
from osmaxx.profile.forms import ProfileForm
from osmaxx.profile.models import Profile


class ProfileView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile/profile_edit.html'

    def get(self, *args, **kwargs):
        profile = self._get_or_create_profile()
        if not self.request.user.email or (profile.unverified_email != self.request.user.email):
            messages.add_message(self.request, messages.INFO, 'Please confirm your email.')
        return super().get(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.id)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Profile successfully updated')
        return reverse('profile:edit_view')

    def _get_or_create_profile(self):
        try:
            profile = Profile.objects.get(associated_user=self.request.user)
        except ObjectDoesNotExist:
            profile = Profile.objects.create(associated_user=self.request.user)
        return profile
