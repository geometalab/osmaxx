from osmaxx.user_messaging.interaction import show_messages
from django.db import transaction, connection, close_old_connections


def message_sepcific_user_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        show_messages(request)
        return response

    return middleware


def send_finished_export_mails(get_response):
    def middleware(request):
        from osmaxx.excerptexport.models.extraction_order import ExtractionOrder

        response = get_response(request)
        with transaction.atomic():
            for extraction_orders in ExtractionOrder.objects.filter(
                export_finished=True, email_sent=False
            ):
                extraction_orders.send_email_if_all_exports_done(request)
        connection.close()
        close_old_connections()
        return response

    return middleware
