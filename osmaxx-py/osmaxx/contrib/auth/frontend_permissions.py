from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from rest_framework import permissions

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
    return user.has_perm('excerptexport.add_extractionorder')


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


class AuthenticatedAndAccessPermission(permissions.BasePermission):
    """
    Allows access only to authenticated users with frontend permissions.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated() and _may_user_access_osmaxx_frontend(request.user)


class HasBBoxAccessPermission(permissions.BasePermission):
    message = 'Accessing this bounding box is not allowed.'

    def has_object_permission(self, request, view, obj):
        return obj.excerpt.is_public or obj.excerpt.owner == request.user


class HasExcerptAccessPermission(permissions.BasePermission):
    message = 'Accessing this excerpt is not allowed.'

    def has_object_permission(self, request, view, obj):
        return obj.is_public or obj.owner == request.user
