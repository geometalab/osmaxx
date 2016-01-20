from django.shortcuts import get_object_or_404, render_to_response
from django.http import StreamingHttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.conf import settings

from .models import ExtractionOrder, Excerpt, OutputFile, BBoxBoundingGeometry
from .models.extraction_order import ExtractionOrderState
from osmaxx.contrib.auth.frontend_permissions import (
    frontend_access_required,
    LoginRequiredMixin,
    FrontendAccessRequiredMixin
)
from .forms import ExportOptionsForm, NewExcerptForm
from excerptconverter import ConverterManager
from osmaxx.utils import private_storage


class NewExtractionOrderView(LoginRequiredMixin, FrontendAccessRequiredMixin, View):
    def get(self, request, excerpt_form_initial_data=None):
        active_excerpts = Excerpt.objects.filter(is_active=True)
        active_bbox_excerpts = active_excerpts.filter(
            bounding_geometry_raw_reference__bboxboundinggeometry__isnull=False
        )
        active_file_excerpts = active_excerpts.filter(
            bounding_geometry_raw_reference__osmosispolygonfilterboundinggeometry__isnull=False)
        view_model = {
            'user': request.user,
            'export_options_form': ExportOptionsForm(ConverterManager.converter_configuration(), auto_id='%s'),
            'new_excerpt_form': NewExcerptForm(auto_id='%s', initial=excerpt_form_initial_data),
            'excerpts': {
                'own_private': active_bbox_excerpts.filter(is_public=False, owner=request.user),
                'own_public': active_bbox_excerpts.filter(is_public=True, owner=request.user),
                'other_public': active_bbox_excerpts.filter(is_public=True).exclude(owner=request.user),
                'countries': active_file_excerpts
            }
        }
        return render_to_response('excerptexport/templates/new_excerpt_export.html', context=view_model,
                                  context_instance=RequestContext(request))

    def post(self, request):
        export_options_form = ExportOptionsForm(
            ConverterManager.converter_configuration(),
            request.POST
        )

        if export_options_form.is_valid():
            export_options = export_options_form.get_export_options()

            extraction_order = None
            if request.POST['form-mode'] == 'existing-excerpt':
                existing_excerpt_id = request.POST['existing_excerpt.id']
                extraction_order = ExtractionOrder.objects.create(
                    excerpt_id=existing_excerpt_id,
                    orderer=request.user,
                    extraction_configuration=export_options
                )

            if request.POST['form-mode'] == 'new-excerpt':
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
                        is_public=form_data['new_excerpt_is_public'],
                        bounding_geometry=bounding_geometry,
                        owner=request.user
                    )

                    extraction_order = ExtractionOrder.objects.create(
                        excerpt=excerpt,
                        orderer=request.user,
                        extraction_configuration=export_options
                    )

                else:
                    messages.error(request, _('Invalid excerpt.'))
                    return self.get(request, new_excerpt_form.data)

            if extraction_order.id:
                converter_manager = ConverterManager(extraction_order)
                converter_manager.execute_converters()

                messages.info(request, _(
                    'Queued extraction order %(id)s. '
                    'The conversion process will start soon.'
                ) % {'id': extraction_order.id})
                return HttpResponseRedirect(
                    reverse('excerptexport:status', kwargs={'extraction_order_id': extraction_order.id})
                )

            else:
                messages.error(request, _('Creation of extraction order "%s" failed.' % extraction_order.id))
                return self.get(request, export_options_form.data)

        else:
            messages.error(request, _('Invalid export options.'))
            return self.get(request, export_options_form.data)


@login_required()
@frontend_access_required()
def list_downloads(request):
    view_context = {
        'host_domain': request.get_host(),
        'extraction_orders': ExtractionOrder.objects.filter(
            orderer=request.user,
            state=ExtractionOrderState.FINISHED
        ).order_by('-id')[:settings.OSMAXX['orders_history_number_of_items']]
    }
    return render_to_response('excerptexport/templates/list_downloads.html', context=view_context,
                              context_instance=RequestContext(request))


def download_file(request, uuid):
    output_file = get_object_or_404(OutputFile, public_identifier=uuid, deleted_on_filesystem=False)
    if not output_file.file:
        return HttpResponseNotFound('<p>No output file attached to output file record.</p>')

    download_file_name = output_file.download_file_name

    # stream file in chunks
    response = StreamingHttpResponse(
        FileWrapper(
            private_storage.open(output_file.file),
        ),
        content_type=output_file.mime_type
    )
    response['Content-Length'] = private_storage.size(output_file.file)
    response['Content-Disposition'] = 'attachment; filename=%s' % download_file_name
    return response


@login_required()
@frontend_access_required()
def extraction_order_status(request, extraction_order_id):
    view_context = {
        'host_domain': request.get_host(),
        'extraction_order': get_object_or_404(ExtractionOrder, id=extraction_order_id, orderer=request.user)
    }
    return render_to_response('excerptexport/templates/extraction_order_status.html', context=view_context,
                              context_instance=RequestContext(request))


@login_required()
@frontend_access_required()
def list_orders(request):
    view_context = {
        'host_domain': request.get_host(),
        'extraction_orders': ExtractionOrder.objects.filter(orderer=request.user)
        .order_by('-id')[:settings.OSMAXX['orders_history_number_of_items']]
    }
    return render_to_response('excerptexport/templates/list_orders.html', context=view_context,
                              context_instance=RequestContext(request))
