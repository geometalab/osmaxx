from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator

OSMAXX_FRONTEND_USER = settings.OSMAXX_AUTHORIZATION['groups']['osmaxx_frontend_user']['group_name']


def frontend_access_required(function=None):
    """
    Decorator for views that checks that the user has the correct access rights,
    redirecting to the information page if necessary.
    """
    access_denied_info_url = reverse_lazy('excerptexport:access_denied')
    actual_decorator = user_passes_test(
        lambda u: user_in_osmaxx_group(u),
        login_url=access_denied_info_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def user_in_osmaxx_group(user):
    """
    Actual test to check if the user is in the frontend user group,
    to give access or deny it. Note: Admins have superpowers.
    """
    if user.is_superuser:
        return True
    group = Group.objects.get(name=OSMAXX_FRONTEND_USER)
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
