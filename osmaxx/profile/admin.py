from django import forms
from django.contrib import admin

from osmaxx.profile.models import Profile


class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['associated_user', 'unverified_email']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['associated_user', 'unverified_email']
    form = ProfileAdminForm
admin.site.register(Profile, ProfileAdmin)  # noqa: E305 expected 2 blank lines after class or function definition, found 0
