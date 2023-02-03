from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin


class RestrictStaffToAdminMiddleware(MiddlewareMixin):
    """
    A middleware that restricts staff members access to administration panels.
    """

    def process_request(self, request):
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "Restrict staff to admin middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RestrictStaffToAdminMiddleware class.")
        if request.user.is_staff and not request.user.is_superuser:
            if request.path.startswith(reverse('admin:index')):
                msg = u'Staff members cannot access the admin page.'
                return HttpResponseForbidden(msg)