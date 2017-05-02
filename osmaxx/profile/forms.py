from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django import forms
from django.utils.translation import ugettext_lazy as _

from osmaxx.profile.models import Profile


class ProfileForm(forms.ModelForm):
    unverified_email = forms.EmailField(max_length=200, required=True, label=_('email address'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            'unverified_email',
        )

    class Meta:
        model = Profile
        fields = ['unverified_email']
