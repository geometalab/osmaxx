from osmaxx.user_messaging.interaction import show_messages


def message_sepcific_user_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        show_messages(request)
        return response

    return middleware