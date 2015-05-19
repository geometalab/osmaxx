import os

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import StreamingHttpResponse, HttpResponseNotFound
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from excerptexport.models import ExtractionOrder, Excerpt, OutputFile, BBoxBoundingGeometry
from excerptexport.models.extraction_order import ExtractionOrderState
from excerptexport import settings as excerptexport_settings
from excerptexport.services.data_conversion_service import trigger_data_conversion
from excerptexport.forms import ExportOptionsForm, NewExcerptForm


private_storage = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT)


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
    def get(self, request, excerpt_form_initial_data=None):
        view_model = {
            'user': request.user,
            'export_options_form': ExportOptionsForm(auto_id='%s'),
            'new_excerpt_form': NewExcerptForm(auto_id='%s', initial=excerpt_form_initial_data),
            'personal_excerpts': Excerpt.objects.filter(is_active=True, is_public=False, owner=request.user,
                                                        bounding_geometry__bboxboundinggeometry__isnull=False),
            'public_excerpts': Excerpt.objects.filter(is_active=True, is_public=True,
                                                      bounding_geometry__bboxboundinggeometry__isnull=False),
            'countries': Excerpt.objects.filter(is_active=True,
                                                bounding_geometry__osmosispolygonfilterboundinggeometry__isnull=False)
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
                form_data = new_excerpt_form.cleaned_data
                bounding_geometry = BBoxBoundingGeometry.create_from_bounding_box_coordinates(
                    form_data['new_excerpt_bounding_box_north'],
                    form_data['new_excerpt_bounding_box_east'],
                    form_data['new_excerpt_bounding_box_south'],
                    form_data['new_excerpt_bounding_box_west']
                )

                excerpt = Excerpt.objects.create(
                    name=form_data['new_excerpt_name'],
                    is_active=True,
                    is_public=form_data['new_excerpt_is_public'] if ('new_excerpt_is_public' in form_data) else False,
                    bounding_geometry=bounding_geometry,
                    owner=request.user
                )

                extraction_order = ExtractionOrder.objects.create(
                    excerpt=excerpt,
                    orderer=request.user
                )

            else:
                return self.get(request, new_excerpt_form.data)

        view_context['extraction_order'] = extraction_order

        export_options_form = ExportOptionsForm(request.POST)
        if export_options_form.is_valid():
            export_options = export_options_form.get_export_options(excerptexport_settings.EXPORT_OPTIONS)
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
    return render(request, 'excerptexport/templates/list_downloads.html', view_context)


def download_file(request, uuid):
    output_file = get_object_or_404(OutputFile, public_identifier=uuid, deleted_on_filesystem=False)
    if not output_file.file:
        return HttpResponseNotFound('<p>No output file attached to output file record.</p>')

    download_file_name = excerptexport_settings.APPLICATION_SETTINGS['download_file_name'] % {
        'id': str(output_file.public_identifier),
        'name': os.path.basename(output_file.file.name)
    }

    # stream file in chunks
    response = StreamingHttpResponse(
        FileWrapper(
            private_storage.open(output_file.file),
            excerptexport_settings.APPLICATION_SETTINGS['download_chunk_size']
        ),
        content_type=output_file.mime_type
    )
    response['Content-Length'] = private_storage.size(output_file.file)
    response['Content-Disposition'] = 'attachment; filename=%s' % download_file_name
    return response


@login_required()
@has_excerptexport_all_permissions()
def extraction_order_status(request, extraction_order_id):
    view_context = {
        'host_domain': request.get_host(),
        'extraction_order': get_object_or_404(ExtractionOrder, id=extraction_order_id, orderer=request.user)
    }
    return render(request, 'excerptexport/templates/extraction_order_status.html', view_context)


@login_required()
@has_excerptexport_all_permissions()
def list_orders(request):
    view_context = {
        'host_domain': request.get_host(),
        'extraction_orders': ExtractionOrder.objects.filter(orderer=request.user)
        .order_by('-id')[:excerptexport_settings.APPLICATION_SETTINGS['orders_history_number_of_items']]
    }
    return render(request, 'excerptexport/templates/list_orders.html', view_context)
