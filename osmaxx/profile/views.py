from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.views import generic

from osmaxx.contrib.auth.frontend_permissions import LoginRequiredMixin
from osmaxx.profile.forms import ProfileForm


class ProfileView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = ProfileForm
    template_name = 'profile/profile_edit.html'

    def get_object(self, queryset=None):
        if self.request.user:
            return self.model.objects.get(pk=self.request.user.id)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Profile successfully updated')
        return reverse('profile:edit_view')
