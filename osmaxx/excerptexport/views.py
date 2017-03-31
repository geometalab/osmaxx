import logging
from collections import OrderedDict

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.datastructures import OrderedSet
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, GenericViewError
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, DeleteView
from django.views.generic.list import ListView

from osmaxx.contrib.auth.frontend_permissions import (
    LoginRequiredMixin,
    EmailRequiredMixin,
)
from osmaxx.conversion_api import statuses
from osmaxx.excerptexport.forms import ExcerptForm, ExistingForm
from osmaxx.excerptexport.models import Excerpt
from osmaxx.excerptexport.models import ExtractionOrder
from osmaxx.excerptexport.signals import postpone_work_until_request_finished
from .models import Export


logger = logging.getLogger(__name__)


def execute_converters(extraction_order, request):
    extraction_order.forward_to_conversion_service(incoming_request=request)


class OrderFormViewMixin(FormMixin):
    def form_valid(self, form):
        extraction_order = form.save(self.request.user)
        postpone_work_until_request_finished(execute_converters, extraction_order, request=self.request)
        messages.info(
            self.request,
            _('Queued extraction order {id}. The conversion process will start soon.').format(
                id=extraction_order.id
            )
        )
        return HttpResponseRedirect(
            reverse('excerptexport:export_list')
        )


class AccessRestrictedBaseView(LoginRequiredMixin, EmailRequiredMixin):
    pass


class OrderNewExcerptView(AccessRestrictedBaseView, OrderFormViewMixin, FormView):
    template_name = 'excerptexport/templates/order_new_excerpt.html'
    form_class = ExcerptForm
order_new_excerpt = OrderNewExcerptView.as_view()


class OrderExistingExcerptView(AccessRestrictedBaseView, OrderFormViewMixin, FormView):
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
            .defer('extraction_order__excerpt__bounding_geometry')
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


class ExportsListView(AccessRestrictedBaseView, ExportsListMixin, ListView):
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
            super().get_queryset().filter(pk__in=self.excerpt_ids)
            .defer('bounding_geometry'), key=lambda x: self.excerpt_ids.index(x.pk)
        )

    def _get_exports_for_excerpt(self, excerpt):
        return self.get_user_exports().\
            filter(extraction_order__excerpt=excerpt).\
            select_related('extraction_order', 'extraction_order__excerpt', 'output_file')\
            .defer('extraction_order__excerpt__bounding_geometry')
export_list = ExportsListView.as_view()


class ExportsDetailView(AccessRestrictedBaseView, ExportsListMixin, ListView):
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


def _social_identification_description(user):
    social_identities = list(user.social_auth.all())
    if social_identities:
        return "identified " + " and ".join(
            "as '{}' by {}".format(soc_id.uid, soc_id.provider) for soc_id in social_identities
        )
    else:
        return "not identified by any social identity providers"


class ExcerptManageListView(ListView):
    model = Excerpt
    context_object_name = 'excerpts'
    template_name = 'excerptexport/excerpt_manage_list.html'

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user, is_public=False, extraction_orders__orderer=user).distinct()
manage_own_excerpts = ExcerptManageListView.as_view()


class DeleteExcerptView(DeleteView):
    model = Excerpt
    context_object_name = 'excerpt'
    template_name = 'excerptexport/excerpt_confirm_delete.html'

    def get_success_url(self):
        return reverse('excerptexport:manage_own_excerpts')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        excerpt = context_data[self.context_object_name]
        context_data['exports'] = Export.objects.filter(extraction_order__excerpt=excerpt)
        return context_data

    def delete(self, request, *args, **kwargs):
        excerpt = self.get_object()
        user = self.request.user
        if user != excerpt.owner:
            raise GenericViewError("User doesn't match the excerpt's owner.")
        if excerpt.is_public:
            raise GenericViewError("No self-defined public excerpts can be deleted.")
        if ExtractionOrder.objects.exclude(orderer=user).count() > 0:
            raise GenericViewError("Others' exports reference this excerpt.")
        if excerpt.has_running_exports:
            logger.error('Deletion not allowed during an active extraction.')
            messages.error(self.request, _('Exports are currently running for this excerpt.'
                                           ' Please try deleting again, when these are finished.'))
            return HttpResponseRedirect(self.get_success_url())

        return super().delete(request, *args, **kwargs)
delete_excerpt = DeleteExcerptView.as_view()
