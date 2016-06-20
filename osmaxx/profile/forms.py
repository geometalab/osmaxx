from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django import forms


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-profileForm'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('profile:edit_view')
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            'email',
        )

    class Meta:
        User = get_user_model()
        model = User
        fields = ['email']
