import os

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import StreamingHttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import permission_required
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator

from excerptexport.models import ExtractionOrder, Excerpt, OutputFile, BoundingGeometry
from excerptexport.models.extraction_order import ExtractionOrderState
from excerptexport import settings
from excerptexport.services.data_conversion_service import trigger_data_conversion
from excerptexport.forms import ExportOptionsForm, NewExcerptForm


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


class NewExtractionOrderView(View):
    @method_decorator(login_required)
    @method_decorator(has_excerptexport_all_permissions())
    def get(self, request):
        view_model = {
            'user': request.user,
            'export_options_form': ExportOptionsForm(auto_id='%s'),
            'new_excerpt_form': NewExcerptForm(auto_id='%s'),
            'personal_excerpts': Excerpt.objects.filter(is_active=True, is_public=False, owner=request.user),
            'public_excerpts': Excerpt.objects.filter(is_active=True, is_public=True),
            'administrative_areas': settings.ADMINISTRATIVE_AREAS
        }
        return render(request, 'excerptexport/templates/new_excerpt_export.html', view_model)


    @method_decorator(login_required)
    @method_decorator(has_excerptexport_all_permissions())
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
            new_excerpt_form = NewExcerptForm(request.POST)
            if new_excerpt_form.is_valid():
                bounding_geometry = BoundingGeometry.create_from_bounding_box_coordinates(
                    new_excerpt_form.cleaned_data['new_excerpt_bounding_box_north'],
                    new_excerpt_form.cleaned_data['new_excerpt_bounding_box_east'],
                    new_excerpt_form.cleaned_data['new_excerpt_bounding_box_south'],
                    new_excerpt_form.cleaned_data['new_excerpt_bounding_box_west']
                )
                bounding_geometry.save()

                excerpt = Excerpt(
                    name=request.POST['new_excerpt_name'],
                    is_active=True,
                    is_public=request.POST['new_excerpt_is_public'] if ('new_excerpt_is_public' in request.POST) else False,
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

        export_options = get_export_options(request.POST, settings.EXPORT_OPTIONS)
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
