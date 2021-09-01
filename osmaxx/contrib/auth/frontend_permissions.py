from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from rest_framework import permissions

from osmaxx.profile.models import Profile


def _may_user_access_this_excerpt(user, excerpt):
    return excerpt.is_public or excerpt.owner == user


def _may_user_access_this_export(user, export):
    return export.extraction_order.orderer == user


def _user_has_validated_email(user):
    try:
        profile = Profile.objects.get(associated_user=user)
    except Profile.DoesNotExist:
        return False
    return profile.has_validated_email()


def validated_email_required(function=None):
    """
    Decorator for views that checks that the user has set a validated email,
    redirecting to the profile page if necessary.
    """
    profile_url = reverse_lazy("profile:edit_view")
    actual_decorator = user_passes_test(
        _user_has_validated_email, login_url=profile_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


class EmailRequiredMixin(object):
    """
    Frontend Access Check Mixin for Class Based Views.
    """

    @method_decorator(validated_email_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AuthenticatedAndAccessPermission(permissions.BasePermission):
    """
    Allows access only to authenticated users with confirmed email address.
    """

    def has_permission(self, request, *args, **kwargs):
        return request.user.is_authenticated and _user_has_validated_email(request.user)


class HasBBoxAccessPermission(permissions.BasePermission):
    message = "Accessing this bounding box is not allowed."

    def has_object_permission(self, request, view, obj, *args, **kwargs):
        return _may_user_access_this_excerpt(request.user, obj.excerpt)


class HasExcerptAccessPermission(permissions.BasePermission):
    message = "Accessing this excerpt is not allowed."

    def has_object_permission(self, request, view, obj, *args, **kwargs):
        return _may_user_access_this_excerpt(request.user, obj)


class HasExportAccessPermission(permissions.BasePermission):
    message = "Accessing this export is not allowed."

    def has_object_permission(self, request, view, obj, *args, **kwargs):
        return _may_user_access_this_export(request.user, obj)
