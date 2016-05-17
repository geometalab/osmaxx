import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound, HttpResponseRedirect, FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from osmaxx.contrib.auth.frontend_permissions import (
    LoginRequiredMixin,
    FrontendAccessRequiredMixin
)
from osmaxx.excerptexport.forms import ExcerptForm, ExistingForm
from osmaxx.utils import get_default_private_storage
from .models import OutputFile, Export


logger = logging.getLogger(__name__)


def execute_converters(extraction_order, request):
    extraction_order.forward_to_conversion_service(incoming_request=request)


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
            reverse('excerptexport:export_list')
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


class ExportsListView(LoginRequiredMixin, FrontendAccessRequiredMixin, ListView):
    template_name = 'excerptexport/exports_list.html'
    context_object_name = 'exports'
    model = Export
    ordering = ['-id']

    def get_queryset(self):
        return super().get_queryset().filter(extraction_order__orderer=self.request.user)
export_list = ExportsListView.as_view()


class AccesssDenied(TemplateView):
    template_name = 'excerptexport/templates/access_denied.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(next_page=self.request.GET.get('next', '/')))
access_denied = AccesssDenied.as_view()


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

    return redirect(request.GET['next'] + '?next=' + request.GET['next'])


def _social_identification_description(user):
    social_identities = list(user.social_auth.all())
    if social_identities:
        return "identified " + " and ".join(
            "as '{}' by {}".format(soc_id.uid, soc_id.provider) for soc_id in social_identities
        )
    else:
        return "not identified by any social identity providers"
