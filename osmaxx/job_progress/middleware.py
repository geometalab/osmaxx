import logging
from datetime import timedelta

from osmaxx.api_client import ConversionApiClient
from osmaxx.conversion_api.statuses import FINAL_STATUSES
from osmaxx.excerptexport.models import Export
from osmaxx.utilities.shortcuts import get_cached_or_set

logger = logging.getLogger(__name__)


class ExportUpdaterMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'user'), (
            "The osmaxx export updater middleware requires Django authentication middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.auth.middleware.AuthenticationMiddleware' before "
            "'osmaxx.job_progress.middleware.ExportUpdaterMiddleware'."
        )
        update_exports_of_request_user(request)


def update_exports_of_request_user(request):
    current_user = request.user
    if current_user.is_anonymous():
        return
    for export in Export.objects.exclude(status__in=FINAL_STATUSES).filter(extraction_order__orderer=current_user):
        update_export_if_stale(export)


def update_export_if_stale(export):
    get_cached_or_set(
        'export_{}_job_progress'.format(export.id),
        update_export, export,
        on_cache_hit=_log_cache_hit,
        timeout=timedelta(minutes=1).total_seconds(),
    )


def update_export(export):
    _log_cache_miss(export)
    client = ConversionApiClient()
    status = client.job_status(export)
    export.set_and_handle_new_status(status)
    if logger.isEnabledFor(logging.DEBUG):
        message = "Fetched, updated and cached Export {export} status: {status}".format(
            export=export.id,
            status=export.get_status_display(),
        )
        logger.debug(message)
    return export.status


def _log_cache_miss(export):
    if not logger.isEnabledFor(logging.INFO):
        return
    message = "Cache miss - Re-fetching progress of pending Export {export}.".format(
        export=export.id,
    )
    logger.info(message)


def _log_cache_hit(cached_value, export):
    if not logger.isEnabledFor(logging.INFO):
        return
    message = (
        "Cache hit - Not re-fetching progress of pending Export {export}, "
        "as it has already been fetched recently. Status then was {status}."
    ).format(
        export=export.id,
        status=export.get_status_display(),
    )
    logger.info(message)
