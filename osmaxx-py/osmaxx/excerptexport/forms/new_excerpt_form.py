from django import forms
from django.utils.translation import gettext_lazy


class NewExcerptForm(forms.Form):
    new_excerpt_name = forms.CharField(label=gettext_lazy('Excerpt name'))
    new_excerpt_bounding_box_north = forms.CharField(label=gettext_lazy('North'))
    new_excerpt_bounding_box_west = forms.CharField(label=gettext_lazy('West'))
    new_excerpt_bounding_box_east = forms.CharField(label=gettext_lazy('East'))
    new_excerpt_bounding_box_south = forms.CharField(label=gettext_lazy('South'))
    new_excerpt_is_public = forms.BooleanField(label=gettext_lazy('Public'), required=False)
