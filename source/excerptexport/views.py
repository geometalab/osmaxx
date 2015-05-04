import os

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response

from django.http import StreamingHttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import permission_required
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from excerptexport.models import ExtractionOrder
from excerptexport.models import Excerpt
from excerptexport.models import OutputFile
from excerptexport.models import BoundingGeometry
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


def access_denied(request):
    return render_to_response('excerptexport/templates/access_denied.html', context=RequestContext(request))


def index(request):
    return render_to_response('excerptexport/templates/index.html', context=RequestContext(request))


class NewExcerptExportViewModel:
    def __init__(self, user):
        self.user = user
        self.personal_excerpts = Excerpt.objects.filter(is_active=True, is_public=False, owner=user)
        self.public_excerpts = Excerpt.objects.filter(is_active=True, is_public=True)

        self.administrative_areas = settings.ADMINISTRATIVE_AREAS
        self.export_options = settings.EXPORT_OPTIONS

    def get_context(self):
        return self.__dict__


@login_required(login_url='/excerptexport/login/')
@has_excerptexport_all_permissions()
def new_excerpt_export(request):
    view_model = NewExcerptExportViewModel(request.user)
    return render(request, 'excerptexport/templates/new_excerpt_export.html', view_model.get_context())


@login_required(login_url='/excerptexport/login/')
@has_excerptexport_all_permissions()
def create_excerpt_export(request):
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


@login_required(login_url='/excerptexport/login/')
@has_excerptexport_all_permissions()
def show_downloads(request):
    view_context = {'host_domain': request.META['HTTP_HOST']}

    files = OutputFile.objects.filter(
        extraction_order__orderer=request.user,
        extraction_order__state=ExtractionOrderState.FINISHED
    )
    view_context['files'] = files
    return render(request, 'excerptexport/templates/show_downloads.html', view_context)


def download_file(request):

    file_id = request.GET['file']
    output_file = get_object_or_404(OutputFile, public_identifier=file_id, deleted_on_filesystem=False)
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


@login_required(login_url='/excerptexport/login/')
@has_excerptexport_all_permissions()
def extraction_order_status(request, extraction_order_id):
    extraction_order = get_object_or_404(ExtractionOrder, id=extraction_order_id, orderer=request.user)
    return render(
        request, 'excerptexport/templates/extraction_order_status.html',
        {'extraction_order': extraction_order, 'host_domain': request.META['HTTP_HOST']}
    )
