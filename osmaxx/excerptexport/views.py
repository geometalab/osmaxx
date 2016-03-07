import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import StreamingHttpResponse, HttpResponseNotFound, HttpResponseRedirect, FileResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from osmaxx.contrib.auth.frontend_permissions import (
    frontend_access_required,
    LoginRequiredMixin,
    FrontendAccessRequiredMixin
)
from osmaxx.excerptexport.forms import ExcerptForm, ExistingForm
from osmaxx.excerptexport.services.shortcuts import get_authenticated_api_client
from osmaxx.utils import get_default_private_storage
from .models import ExtractionOrder, OutputFile
from .models.extraction_order import ExtractionOrderState


logger = logging.getLogger(__name__)


def execute_converters(extraction_order, request):
    get_authenticated_api_client().create_job(extraction_order, request=request)


class OrderFormViewMixin(FormMixin):
    def form_valid(self, form):
        extraction_order = form.save(self.request.user)
        execute_converters(extraction_order, request=self.request)
        messages.info(
            self.request,
            _('Queued extraction order {id}. The conversion process will start soon.').format(
                id=extraction_order.id
            )
        )
        return HttpResponseRedirect(
            reverse('excerptexport:status', kwargs={'extraction_order_id': extraction_order.id})
        )


class OrderNewExcerptView(LoginRequiredMixin, FrontendAccessRequiredMixin, OrderFormViewMixin, FormView):
    template_name = 'excerptexport/templates/order_new_excerpt.html'
    form_class = ExcerptForm


order_new_excerpt = OrderNewExcerptView.as_view()


class OrderExistingExcerptView(LoginRequiredMixin, FrontendAccessRequiredMixin, OrderFormViewMixin, FormView):
    template_name = 'excerptexport/templates/order_existing_excerpt.html'
    form_class = ExistingForm

    def get_form_class(self):
        return super().get_form_class().get_dynamic_form_class(self.request.user)

order_existing_excerpt = OrderExistingExcerptView.as_view()


class DownloadListView(LoginRequiredMixin, FrontendAccessRequiredMixin, ListView):
    template_name = 'excerptexport/templates/list_downloads.html'
    context_object_name = 'extraction_orders'

    def get_queryset(self):
        return ExtractionOrder.objects.filter(
            orderer=self.request.user,
            state=ExtractionOrderState.FINISHED
        ).order_by('-id')

list_downloads = DownloadListView.as_view()


def download_file(request, uuid):
    output_file = get_object_or_404(OutputFile, public_identifier=uuid, deleted_on_filesystem=False)
    if not output_file.file:
        return HttpResponseNotFound('<p>No output file attached to output file record.</p>')

    download_file_name = output_file.download_file_name
    private_storage = get_default_private_storage()

    # stream file in chunks
    response = FileResponse(
        private_storage.open(output_file.file),
        content_type=output_file.mime_type
    )
    response['Content-Length'] = private_storage.size(output_file.file)
    response['Content-Disposition'] = 'attachment; filename=%s' % download_file_name
    return response


class OwnershipRequiredMixin(SingleObjectMixin):
    owner = 'owner'

    def get_object(self, queryset=None):
        o = super().get_object(queryset)
        if getattr(o, self.owner) != self.request.user:
            raise PermissionDenied
        return o


class ExtractionOrderView(LoginRequiredMixin, FrontendAccessRequiredMixin, OwnershipRequiredMixin, DetailView):
    template_name = 'excerptexport/templates/extraction_order_status.html'
    context_object_name = 'extraction_order'
    model = ExtractionOrder
    pk_url_kwarg = 'extraction_order_id'
    owner = 'orderer'

extraction_order_status = ExtractionOrderView.as_view()


@login_required()
@frontend_access_required()
def list_orders(request):
    extraction_orders = ExtractionOrder.objects.filter(orderer=request.user)
    view_context = {
        'extraction_orders': extraction_orders.order_by('-id')
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
        email_message = (  # Intentionally untranslated, as this goes to the administrator(s), not the user.
            '''Hi Admin!
            User '{username}' ({identification_description}) claims to be {first_name} {last_name} ({email})
            and requests access for Osmaxx.
            If {username} shall be granted access, go to {admin_url} and add {username} to group '{frontend_group}'.
            '''
        ).format(
            username=request.user.username,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            email=request.user.email,
            identification_description=_social_identification_description(request.user),
            admin_url=request.build_absolute_uri(reverse('admin:auth_user_change', args=(request.user.id,))),
            frontend_group=settings.OSMAXX_FRONTEND_USER_GROUP,
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


def _social_identification_description(user):
    social_identities = list(user.social_auth.all())
    if social_identities:
        return "identified " + " and ".join(
            "as '{}' by {}".format(soc_id.uid, soc_id.provider) for soc_id in social_identities
        )
    else:
        return "not identified by any social identity providers"
