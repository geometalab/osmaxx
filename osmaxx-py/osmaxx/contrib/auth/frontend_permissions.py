from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator

FRONTEND_USER_GROUP = settings.OSMAXX_FRONTEND_USER_GROUP


def frontend_access_required(function=None):
    """
    Decorator for views that checks that the user has the correct access rights,
    redirecting to the information page if necessary.
    """
    access_denied_info_url = reverse_lazy('excerptexport:access_denied')
    actual_decorator = user_passes_test(
        _may_user_access_osmaxx_frontend,
        login_url=access_denied_info_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def _may_user_access_osmaxx_frontend(user):
    """
    Actual test to check if the user is in the frontend user group,
    to give access or deny it. Note: Admins have superpowers.
    """
    if user.is_superuser:
        return True
    group = Group.objects.get(name=FRONTEND_USER_GROUP)
    return group in user.groups.all()


class LoginRequiredMixin(object):
    """
    Login required Mixin for Class Based Views.
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class FrontendAccessRequiredMixin(object):
    """
    Frontend Access Check Mixin for Class Based Views.
    """
    @method_decorator(frontend_access_required)
    def dispatch(self, *args, **kwargs):
        return super(FrontendAccessRequiredMixin, self).dispatch(*args, **kwargs)
