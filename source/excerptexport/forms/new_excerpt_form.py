from django import forms
from django.utils.translation import gettext_lazy


class NewExcerptForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewExcerptForm, self).__init__(*args, **kwargs)

        self.fields['new_excerpt_name'] = forms.CharField(label=gettext_lazy('Excerpt name'))
        self.fields['new_excerpt_bounding_box_north'] = forms.CharField(label=gettext_lazy('North'))
        self.fields['new_excerpt_bounding_box_west'] = forms.CharField(label=gettext_lazy('West'))
        self.fields['new_excerpt_bounding_box_east'] = forms.CharField(label=gettext_lazy('East'))
        self.fields['new_excerpt_bounding_box_south'] = forms.CharField(label=gettext_lazy('South'))
        self.fields['new_excerpt_is_public'] = forms.BooleanField(label=gettext_lazy('Public'))
