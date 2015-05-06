from django import forms
from django.utils.translation import gettext_lazy


class NewExcerptForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewExcerptForm, self).__init__(*args, **kwargs)

        self.fields['new_excerpt.name'] = forms.CharField(label=gettext_lazy('Excerpt name'))
        self.fields['new_excerpt.boundingBox.north'] = forms.CharField(label=gettext_lazy('North'))
        self.fields['new_excerpt.boundingBox.west'] = forms.CharField(label=gettext_lazy('West'))
        self.fields['new_excerpt.boundingBox.east'] = forms.CharField(label=gettext_lazy('East'))
        self.fields['new_excerpt.boundingBox.south'] = forms.CharField(label=gettext_lazy('South'))
        self.fields['new_excerpt.is_public'] = forms.BooleanField(label=gettext_lazy('Public'))
