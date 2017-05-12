import logging
from datetime import timedelta

import requests
from requests import HTTPError

from osmaxx.api_client import ConversionApiClient
from osmaxx.conversion import status
from osmaxx.excerptexport.models import Export
from osmaxx.utils.shortcuts import get_cached_or_set

logger = logging.getLogger(__name__)


class ExportUpdaterMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'user'), (
            "The osmaxx export updater middleware requires Django authentication middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.auth.middleware.AuthenticationMiddleware' before "
            "'osmaxx.job_progress.middleware.ExportUpdaterMiddleware'."
        )
        try:
            update_exports_of_request_user(request)
        except:  # noqa:
            # Intentionally catching all non-system-exiting exceptions here, because this middleware must never* raise.
            # (This middleware does processing that needs the current request,
            # but is ultimately unrelated to the request.
            # So, whatever happens, this middleware shouldn't let the request processing fail.)
            #
            # * unless improperly configured (see assert above)
            logger.exception("Failed to update statuses of pending requests.")


def handle_unsent_exports(user):
    for export in Export.objects.\
            exclude(status__in=status.FINAL_STATUSES).\
            filter(extraction_order__orderer=user, conversion_service_job_id__isnull=True):
        if export.update_is_overdue:
            export.status = status.FAILED
            export.save()


def update_exports_of_request_user(request):
    current_user = request.user
    if current_user.is_anonymous:
        return

    handle_unsent_exports(user=current_user)

    pending_exports = Export.objects.\
        exclude(status__in=status.FINAL_STATUSES).\
        filter(extraction_order__orderer=current_user, conversion_service_job_id__isnull=False)
    for export in pending_exports:
        try:
            update_export_if_stale(export, request=request)
        except HTTPError as e:
            if e.response.status_code == requests.codes['not_found']:
                logger.exception("Export #%s doesn't exist on the conversion service.", export.id)
                export.status = status.FAILED
                export.save()
            else:
                logger.exception("Failed to update status of pending export #%s.", export.id)
        except:  # noqa:
            # Intentionally catching all non-system-exiting exceptions here, so that the loop can continue
            # and (try) to update the other pending exports.
            logger.exception("Failed to update status of pending export #%s.", export.id)


def update_export_if_stale(export, *, request):
    get_cached_or_set(
        'export_{}_job_progress'.format(export.id),
        update_export, export, request=request,
        on_cache_hit=_log_cache_hit,
        timeout=timedelta(minutes=1).total_seconds(),
    )


def update_export(export, *, request):
    _log_cache_miss(export)
    client = ConversionApiClient()
    status = client.job_status(export)
    export.set_and_handle_new_status(status, incoming_request=request)
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


def _log_cache_hit(cached_value, export, **_):
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
