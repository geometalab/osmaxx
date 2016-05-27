import logging
from collections import OrderedDict

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.datastructures import OrderedSet
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from osmaxx.contrib.auth.frontend_permissions import (
    LoginRequiredMixin,
    FrontendAccessRequiredMixin
)
from osmaxx.conversion_api import statuses
from osmaxx.excerptexport.forms import ExcerptForm, ExistingForm
from osmaxx.excerptexport.models import Excerpt
from .models import Export


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


class OwnershipRequiredMixin(SingleObjectMixin):
    owner = 'owner'

    def get_object(self, queryset=None):
        o = super().get_object(queryset)
        if getattr(o, self.owner) != self.request.user:
            raise PermissionDenied
        return o


class ExportsListMixin:
    _filterable_statuses = frozenset({statuses.FINISHED, statuses.FAILED})

    @property
    def excerpt_ids(self):
        if not hasattr(self, '_excerpt_ids'):
            self._excerpt_ids = list(
                OrderedSet(
                    self.get_user_exports()
                    .values_list('extraction_order__excerpt', flat=True)
                )
            )
        return self._excerpt_ids

    @property
    def status_choices(self):
        return [choice for choice in Export.STATUS_CHOICES if choice[0] in self._filterable_statuses]

    def get_user_exports(self):
        return self._filter_exports(
            Export.objects.filter(extraction_order__orderer=self.request.user)
        ).order_by('-updated_at', '-finished_at')

    def _filter_exports(self, query):
        status_filter = self.request.GET.get('status', None)
        if status_filter in self._filterable_statuses:
            return query.filter(status=status_filter)
        return query

    def _get_extra_context_data(self):
        return dict(
            status_choices=self.status_choices,
            status_filter=self.request.GET.get('status', None),
        )


class ExportsListView(LoginRequiredMixin, FrontendAccessRequiredMixin, ExportsListMixin, ListView):
    template_name = 'excerptexport/export_list.html'
    context_object_name = 'excerpts'
    model = Excerpt
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(self._get_extra_context_data())
        context_data['excerpt_list_with_exports'] = OrderedDict(
            (excerpt, self._get_exports_for_excerpt(excerpt)) for excerpt in context_data[self.context_object_name]
        )
        return context_data

    def get_queryset(self):
        return sorted(
            super().get_queryset().filter(pk__in=self.excerpt_ids), key=lambda x: self.excerpt_ids.index(x.pk)
        )

    def _get_exports_for_excerpt(self, excerpt):
        return self.get_user_exports().\
            filter(extraction_order__excerpt=excerpt).\
            select_related('extraction_order', 'extraction_order__excerpt', 'output_file')
export_list = ExportsListView.as_view()


class ExportsDetailView(LoginRequiredMixin, FrontendAccessRequiredMixin, ExportsListMixin, ListView):
    template_name = 'excerptexport/export_detail.html'
    context_object_name = 'exports'
    model = Export
    pk_url_kwarg = 'id'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(self._get_extra_context_data())
        return context_data

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is None:
            raise AttributeError("ExportsDetailView must be called with an Excerpt pk.")
        queryset = self.get_user_exports()\
            .select_related('extraction_order', 'extraction_order__excerpt', 'output_file')\
            .filter(extraction_order__excerpt__pk=pk)
        return queryset
export_detail = ExportsDetailView.as_view()


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
