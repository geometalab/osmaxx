import logging

from django import forms
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import StreamingHttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from django.conf import settings
from osmaxx.excerptexport.services.shortcuts import get_authenticated_api_client
from .models import ExtractionOrder, OutputFile
from .models.extraction_order import ExtractionOrderState
from osmaxx.contrib.auth.frontend_permissions import (
    frontend_access_required,
    LoginRequiredMixin,
    FrontendAccessRequiredMixin
)
from osmaxx.excerptexport.forms.excerpt_export_form import ExcerptOrderForm
from osmaxx.excerptexport.forms.excerpt_order_form_helpers import get_existing_excerpt_choices_shortcut
from osmaxx.utils import private_storage


logger = logging.getLogger(__name__)


def execute_converters(extraction_order, callback_host, protocol):
    get_authenticated_api_client().create_job(extraction_order, callback_host=callback_host, protocol=protocol)


class OrderFormView(LoginRequiredMixin, FrontendAccessRequiredMixin, FormView):
    template_name = 'excerptexport/templates/excerpt_form.html'
    form_class = ExcerptOrderForm

    def get_form_class(self):
        klass = super().get_form_class()
        klass.declared_fields['existing_excerpts'] = forms.ChoiceField(
            label=_('Excerpt'),
            required=True,
            widget=forms.Select(
                attrs={'size': 10},
            ),
            choices=get_existing_excerpt_choices_shortcut(self.request.user),
        )
        return klass

    def form_valid(self, form):
        extraction_order = form.save(self.request.user)
        request_host = self.request.get_host()
        request_protocol = 'https' if self.request.is_secure() else 'http'
        execute_converters(extraction_order, callback_host=request_host, protocol=request_protocol)
        messages.info(
            self.request,
            _('Queued extraction order {id}. The conversion process will start soon.').format(
                id=extraction_order.id
            )
        )
        return HttpResponseRedirect(
            reverse('excerptexport:status', kwargs={'extraction_order_id': extraction_order.id})
        )

order_form_view = OrderFormView.as_view()


@login_required()
@frontend_access_required()
def list_downloads(request):
    view_context = {
        'protocol': request.scheme,
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
            settings.OSMAXX['download_chunk_size']
        ),
        content_type=output_file.mime_type
    )
    response['Content-Length'] = private_storage.size(output_file.file)
    response['Content-Disposition'] = 'attachment; filename=%s' % download_file_name
    return response


def _update_progress(extraction_order):
    conversion_client = get_authenticated_api_client()
    conversion_client.update_order_status(extraction_order)


@login_required()
@frontend_access_required()
def extraction_order_status(request, extraction_order_id):
    extraction_order = get_object_or_404(ExtractionOrder, id=extraction_order_id, orderer=request.user)

    # Order status will be updated by callback from API. This is just for a failure situation of the API.
    if extraction_order.state < ExtractionOrderState.FINISHED:
        _update_progress(extraction_order)

    view_context = {
        'protocol': request.scheme,
        'host_domain': request.get_host(),
        'extraction_order': extraction_order,
    }
    return render_to_response('excerptexport/templates/extraction_order_status.html', context=view_context,
                              context_instance=RequestContext(request))


@login_required()
@frontend_access_required()
def list_orders(request):
    extraction_orders = ExtractionOrder.objects.filter(orderer=request.user)

    # Order status will be updated by callback from API. This is just for a failure situation of the API.
    for extraction_order in extraction_orders.filter(state__lt=ExtractionOrderState.FINISHED):
        _update_progress(extraction_order)

    view_context = {
        'protocol': request.scheme,
        'host_domain': request.get_host(),
        'extraction_orders': extraction_orders.order_by('-id')[:settings.OSMAXX['orders_history_number_of_items']]
    }
    return render_to_response('excerptexport/templates/list_orders.html', context=view_context,
                              context_instance=RequestContext(request))


def access_denied(request):
    view_context = {
        'next_page': request.GET['next']
    }
    return render_to_response('excerptexport/templates/access_denied.html', context=view_context,
                              context_instance=RequestContext(request))


@login_required()
def request_access(request):
    user_administrator_email = settings.OSMAXX['ACCOUNT_MANAGER_EMAIL']
    if not user_administrator_email:
        logging.exception(
            "You don't have an user account manager email address defined. Please set OSMAXX_ACCOUNT_MANAGER_EMAIL."
        )
        messages.error(
            request,
            _('Sending of access request failed. Please contact an administrator.')
        )
    else:
        email_message = _(
            '''Hi Admin!
            {first_name} {last_name} ({email}) requests access for Osmaxx. Please activate the user {username}.
            '''
        ).format(
            username=request.user.username,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            email=request.user.email,
        )

        try:
            send_mail('Request access for Osmaxx', email_message, settings.DEFAULT_FROM_EMAIL,
                      [user_administrator_email], fail_silently=True)
            messages.success(
                request,
                _('Your access request has been sent successfully. '
                  'You will receive an email when your account is ready.')
            )
        except Exception as exception:
            logging.exception("Sending access request e-mail failed: {0}, \n{1}".format(exception, email_message))
            messages.error(
                request,
                _('Sending of access request failed. Please contact an administrator.')
            )

    return redirect(request.GET['next']+'?next='+request.GET['next'])
