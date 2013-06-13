from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import never_cache
from django.views.generic import View

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin


class AdminLoginView(LoginRequiredMixin, View):
    """
    This view is used to redirect users to the default login page and
    show a permission denied page when they come back if they're not
    staff. Staff users get handled by the AdminSite before this gets
    called, so a logged in staff user will never hit this view.
    """

    def get(self, request):
        if not self.request.user.is_staff:
            raise PermissionDenied()
        # If a user is staff they should be handled automatically by the
        # adminsite. If not the *required mixins will handle the user.
        raise AssertionError("This point should never be reached.")


class DefaultSiteLoginPageMixin(object):
    """
    An AdminSite mixin which replaces the login view with the default
    side-wide login view.
    """

    # Log in users with the normal login view instead of the admin's
    # special one.
    @never_cache
    def login(self, request, extra_context=None):
        return AdminLoginView.as_view()(request)

    def register_django_default_apps(self):
        """
        Register Django's built in models that normally show in the
        admin (django.contrib.auth and django.contrib.sites).
        """
        from django.contrib.auth.admin import UserAdmin, GroupAdmin
        from django.contrib.auth.models import User, Group

        # django.contrib.auth
        self.register(Group, GroupAdmin)
        self.register(User, UserAdmin)

        from django.contrib.sites.admin import SiteAdmin
        from django.contrib.sites.models import Site
        # django.contrib.sites
        self.register(Site, SiteAdmin)


class DefaultSiteLoginPageAdminSite(
        DefaultSiteLoginPageMixin,
        admin.AdminSite):
    """
    An AdminSite implementation which delegates to the default login
    view to log in to the admin site.
    """
