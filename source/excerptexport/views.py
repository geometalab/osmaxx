import os
import sys

from django import forms
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import StreamingHttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import permission_required
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from excerptexport.models import ExtractionOrder, Excerpt, OutputFile, BoundingGeometry
from excerptexport.models.extraction_order import ExtractionOrderState
from excerptexport import settings
from excerptexport.services.data_conversion_service import trigger_data_conversion


def has_excerptexport_all_permissions():
    excerpt_export_permissions = [
        'excerptexport.add_boundinggeometry',
        'excerptexport.change_boundinggeometry',
        'excerptexport.add_excerpt',
        'excerptexport.change_excerpt',
        'excerptexport.add_extractionorder',
        'excerptexport.change_extractionorder',
    ]
    # This is a simple hack, instead of displaying a login page, it shows a permission denied page if the user is
    # logged in
    login_url = reverse_lazy('excerptexport:access_denied')
    return permission_required(excerpt_export_permissions, login_url=login_url, raise_exception=False)


class NewExtractionOrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewExtractionOrderForm, self).__init__(*args, **kwargs)
        for export_option_key, export_option in settings.EXPORT_OPTIONS.items():
            formats = ()
            for format_key, format in export_option['formats'].items():
                field_name = 'export_options.'+export_option_key+'.formats.'+format_key
                formats += ((field_name , format['name']),)
            self.fields['export_options.'+export_option_key+'.formats'] = forms.MultipleChoiceField(choices=formats, label=export_option['name'], required=False, widget=forms.CheckboxSelectMultiple)

            for option_config_key, option_config in export_option['options'].items():
                field_name = 'export_options.'+export_option_key+'.options.'+option_config_key
                # TODO refactor config and replace select and radio by choice
                if option_config['type'] == 'select' or option_config['type'] == 'radio' or option_config['type'] == 'choice':
                    choices = ()
                    if 'values' in option_config.keys():
                        for option in option_config['values']:
                            choices += ((option['name'], option['label']),)

                    if (not 'groups' in option_config.keys()) and 'values' in option_config.keys() and (len(option_config['values']) < 5):
                        self.fields[field_name] = forms.ChoiceField(label=option_config['label'], choices=choices, widget=forms.RadioSelect(), initial=option_config['default'] or None)
                        print(choices)
                    else:
                        if option_config['groups']:
                            for group in option_config['groups']:
                                choice_group = ()
                                for option in group['values']:
                                    choice_group += ((option['name'], option['label']),)
                                choices += ((group['name'], choice_group),)
                        self.fields[field_name] = forms.ChoiceField(label=option_config['label'], choices=choices, initial=option_config['default'] or None)


class NewExtractionOrderView(View):
    # TODO
    #@login_required()
    #@has_excerptexport_all_permissions()
    def get(self, request):
        view_model = {
            'user': request.user,
            'form': NewExtractionOrderForm(),
            'personal_excerpts': Excerpt.objects.filter(is_active=True, is_public=False, owner=request.user),
            'public_excerpts': Excerpt.objects.filter(is_active=True, is_public=True),
            'administrative_areas': settings.ADMINISTRATIVE_AREAS,
            'export_options': settings.EXPORT_OPTIONS
        }
        return render(request, 'excerptexport/templates/new_excerpt_export.html', view_model)

    # TODO
    #@login_required()
    #@has_excerptexport_all_permissions()
    def post(self, request):
        view_context = {}
        if request.POST['form-mode'] == 'existing_excerpt':
            existing_excerpt_id = request.POST['existing_excerpt.id']
            view_context = {'excerpt': existing_excerpt_id}
            extraction_order = ExtractionOrder.objects.create(
                excerpt_id=existing_excerpt_id,
                orderer=request.user
            )

        if request.POST['form-mode'] == 'create_new_excerpt':
            bounding_geometry = BoundingGeometry.create_from_bounding_box_coordinates(
                request.POST['new_excerpt.boundingBox.north'],
                request.POST['new_excerpt.boundingBox.east'],
                request.POST['new_excerpt.boundingBox.south'],
                request.POST['new_excerpt.boundingBox.west']
            )
            bounding_geometry.save()

            excerpt = Excerpt(
                name=request.POST['new_excerpt.name'],
                is_active=True,
                is_public=request.POST['new_excerpt.is_public'] if ('new_excerpt.is_public' in request.POST) else False,
                bounding_geometry=bounding_geometry
            )
            excerpt.owner = request.user
            excerpt.save()

            view_context = {'excerpt': excerpt, 'bounding_geometry': bounding_geometry}
            extraction_order = ExtractionOrder.objects.create(
                excerpt=excerpt,
                orderer=request.user
            )

        view_context['extraction_order'] = extraction_order

        view_context['use_existing'] = 'existing_excerpt_id' in vars()  # TODO: The view should not have to know
        export_options = get_export_options(request.POST, settings.EXPORT_OPTIONS)
        view_context['options'] = export_options

        trigger_data_conversion(extraction_order, export_options)

        response = render_to_response(
            'excerptexport/templates/create_excerpt_export.html',
            view_context,
            context_instance=RequestContext(request)
        )
        if extraction_order.id:
            response['Refresh'] = '5; http://' + request.META['HTTP_HOST'] + reverse(
                'excerptexport:status',
                kwargs={'extraction_order_id': extraction_order.id}
            )
        return response


@login_required()
@has_excerptexport_all_permissions()
def list_downloads(request):
    view_context = {
        'host_domain': request.get_host(),
        'extraction_orders': ExtractionOrder.objects.filter(
            orderer=request.user,
            state=ExtractionOrderState.FINISHED
        )
    }
    return render(request, 'excerptexport/templates/show_downloads.html', view_context)


def download_file(request, uuid):
    output_file = get_object_or_404(OutputFile, public_identifier=uuid, deleted_on_filesystem=False)
    if not output_file.file:
        return HttpResponseNotFound('<p>No output file attached to output file record.</p>')

    download_file_name = settings.APPLICATION_SETTINGS['download_file_name'] % {
        'id': str(output_file.public_identifier),
        'name': os.path.basename(output_file.file.name)
    }
    # abspath usage:  settings.APPLICATION_SETTINGS['data_directory'] may contain '../',
    #                 so use abspath to strip it
    # basepath usage: django stores the absolute path of a file but if we use the location from settings,
    #                 the files are more movable -> so we only use the name of the file
    absolute_file_path = os.path.abspath(
        settings.APPLICATION_SETTINGS['data_directory'] + '/' + os.path.basename(output_file.file.name)
    )

    # stream file in chunks
    response = StreamingHttpResponse(
        FileWrapper(
            open(absolute_file_path),
            settings.APPLICATION_SETTINGS['download_chunk_size']
        ),
        content_type=output_file.mime_type
    )
    response['Content-Length'] = os.path.getsize(absolute_file_path)
    response['Content-Disposition'] = 'attachment; filename=%s' % download_file_name
    return response


def get_export_options(requestPostValues, optionConfig):
    # post values naming schema:
    # formats: "export_options.{{ export_option_key }}.formats"
    # options: "'export_options.{{ export_option_key }}.options.{{ export_option_config_key }}"
    export_options = {}
    for export_option_key, export_option in optionConfig.items():
        export_options[export_option_key] = {}
        export_options[export_option_key]['formats'] = requestPostValues.getlist(
            'export_options.'+export_option_key+'.formats'
        )

        for export_option_config_key, export_option_config in export_option['options'].items():
            export_options[export_option_key][export_option_config_key] = requestPostValues.getlist(
                'export_options.'+export_option_key+'.options.'+export_option_config_key
            )

    return export_options


@login_required()
@has_excerptexport_all_permissions()
def extraction_order_status(request, extraction_order_id):
    view_context = {
        'host_domain': request.get_host(),
        'extraction_order': get_object_or_404(ExtractionOrder, id=extraction_order_id, orderer=request.user)
    }
    return render(request, 'excerptexport/templates/extraction_order_status.html',view_context)


@login_required()
@has_excerptexport_all_permissions()
def list_orders(request):
    view_context = {
        'host_domain': request.get_host(),
        'extraction_orders': ExtractionOrder.objects.filter(orderer=request.user)
            .order_by('-id')[:settings.APPLICATION_SETTINGS['orders_history_number_of_items']]
    }
    return render(request, 'excerptexport/templates/list_orders.html', view_context)
