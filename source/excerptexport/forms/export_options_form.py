from django import forms

from excerptexport import settings


class ExportOptionsForm(forms.Form):
    max_items_radio = 5

    def __init__(self, *args, **kwargs):
        super(ExportOptionsForm, self).__init__(*args, **kwargs)
        for export_option_key, export_option in settings.EXPORT_OPTIONS.items():
            self.create_checkboxes(
                'export_options.'+export_option_key+'.formats', export_option['name'],
                export_option['formats'].items()
            )

            for option_config_key, option_config in export_option['options'].items():
                if option_config['type'] == 'choice':
                    self.create_choice(
                        'export_options.'+export_option_key+'.options.'+option_config_key,
                        option_config['label'],
                        option_config['groups'] if 'groups' in option_config.keys() else None,
                        option_config['values'] if 'values' in option_config.keys() else None,
                        option_config['default'] if 'default' in option_config.keys() else None
                    )

    # create choice element (select or radio if #items <= max_items_radio and only flat values)
    def create_choice(self, field_name, field_label, groups, values, default):
        choices = ()
        if values:
            for option in values:
                choices += ((option['name'], option['label']),)

        if (not groups) and values and (len(values) <= self.max_items_radio):
            self.fields[field_name] = forms.ChoiceField(
                label=field_label,
                choices=choices,
                widget=forms.RadioSelect(),
                initial=default
            )
        else:
            if groups:
                for group in groups:
                    choice_group = ()
                    for option in group['values']:
                        choice_group += ((option['name'], option['label']),)
                    choices += ((group['name'], choice_group),)
            self.fields[field_name] = forms.ChoiceField(label=field_label, choices=choices, initial=default)

    # create a checkbox group (all elements have same name but different values)
    def create_checkboxes(self, group_key, group_label, items):
        values = ()
        for key, element in items:
            values += ((key, element['name']),)

        self.fields[group_key] = forms.MultipleChoiceField(
            choices=values,
            label=group_label,
            required=False,
            widget=forms.CheckboxSelectMultiple
        )

    # create export options tree (like export options settings) from flat form values
    def get_export_options(self, option_config):
        # post values naming schema:
        # formats: "export_options_{{ export_option_key }}_formats"
        # options: "'export_options_{{ export_option_key }}_options_{{ export_option_config_key }}"
        export_options = {}
        for export_option_key, export_option in option_config.items():
            export_options[export_option_key] = {}
            export_options[export_option_key]['formats'] = \
                self.cleaned_data['export_options.'+export_option_key+'.formats']

            for export_option_config_key, export_option_config in export_option['options'].items():
                export_options[export_option_key][export_option_config_key] = \
                    self.cleaned_data['export_options.'+export_option_key+'.options.'+export_option_config_key]

        return export_options
