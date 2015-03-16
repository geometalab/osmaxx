from django.test import TestCase
from django.shortcuts import render
from django.template import Context, Template

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from pprint import pprint


class PartialsTestCase(TestCase):
    def test_rendering_select_with_groups(self):
        context = Context({
            'coordinate_reference_system': {
                'label': 'Coordinate reference system',
                'type': 'select',
                'select_multiple': False,
                'default': 'pseudomerkator',
                'groups': [
                    {
                        'name': 'Global coordinate reference systems',
                        'values': [
                            { 'name': 'pseudomerkator', 'label': 'Pseudo merkator' },
                            { 'name': 'wgs72', 'label': 'WGS 72' },
                            { 'name': 'wgs84', 'label': 'WGS 84' }
                        ]
                    },
                    {
                        'name': 'UTM zones for your export',
                        'values': [
                            { 'name': 'utm32', 'label': 'UTM zone 32' },
                            { 'name': 'utm33', 'label': 'UTM zone 33' }
                        ]
                    }
                ]
            }
        })
        template = Template("{% spaceless %}{% include 'excerptexport/partials/select.html' with element=coordinate_reference_system name='coordinate_reference_system' %}{% endspaceless %}")
        renderedView = template.render(context)
        expextedRenderedTemplate = Template("""{% spaceless %}
<select name="coordinate_reference_system" id="coordinate_reference_system">
    <optgroup label="Global coordinate reference systems">
        <option value="pseudomerkator">Pseudo merkator</option>
        <option value="wgs72">WGS 72</option>
        <option value="wgs84">WGS 84</option>
    </optgroup>
    <optgroup label="UTM zones for your export">
        <option value="utm32">UTM zone 32</option>
        <option value="utm33">UTM zone 33</option>
    </optgroup>
</select>
{% endspaceless %}""").render(Context({}))

        self.assertEqual(renderedView, expextedRenderedTemplate)