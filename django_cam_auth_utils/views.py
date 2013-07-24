"""
This module provides login views for authentication methods commonly
used at Cambridge University.

* ``RemoteUserLoginView`` is sutable for use with Raven when just the
  login URL is protected (e.g. ``accounts/login``).
* ``ShibbolethRemoteUserLoginView`` acts as ``RemoteUserLoginView``
  would when using Raven. It's only sutable for use with just Cambridge
  shib users.
"""

from django.conf import settings
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import resolve_url
from django.utils.cache import add_never_cache_headers
from django.utils.http import is_safe_url
from django.views.generic import RedirectView

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin


class NeverCacheMixin(object):
    """
    A View mixin which marks the response as not cachable by setting
    appropreate headers.
    """
    def dispatch(self, *args, **kwargs):
        response = super(NeverCacheMixin, self).dispatch(*args, **kwargs)
        add_never_cache_headers(response)
        return response


class RemoteUserLoginView(NeverCacheMixin, RedirectView):
    """
    Handles logging in users when they hit a url which is protected by
    the webserver we're running in. The webserver needs to provide a
    REMOTE_USER variable containing the authenticated username. (The name
    of this variable is configurable with the header attribute).

    This view is an alternative to RemoteUserMiddleware and should be used
    when only one url is protected by the webserver. RemoteUserMiddleware
    expects the entire application to be protected and requires REMOTE_USER
    to be set for every request. This view only requires it to be present
    when actually logging in.

    RemoteUserBackend should be present in AUTHENTICATION_BACKENDS.
    """
    permanent = False

    header = "REMOTE_USER"

    def get_redirect_url(self, **kwargs):
        redirect_to = self.request.GET.get("next", "")

        can_use_next = (
            bool(redirect_to) and
            is_safe_url(url=redirect_to, host=self.request.get_host())
        )

        if not can_use_next:
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        self.login_from_remote_user()
        return redirect_to

    def login_from_remote_user(self):
        # We require the REMOTE_USER (or whatever it's set to) to be present
        # at all times, as the webserver should take care of authenticating
        # users before they hit our application.
        try:
            username = self.clean_username(
                self.request.META[self.header])
        except KeyError:
            raise ImproperlyConfigured(
                "No auth header \"{}\" received from webserver in META"
                .format(self.header)
            )

        if self.request.user.is_authenticated():
            if username == self.request.user.username:
                # The user is already logged in, nothing to do
                return

        # Defer to the auth backend to create a user and log them in.
        # It's expected that the auth backend is (or is compatible with)
        # RemoteUserBackend.
        user = auth.authenticate(remote_user=username)
        if user:
            self.request.user = user
            auth.login(self.request, user)

            return

        # This shouldn't normally happen, but if authenticate() rejects
        # the user they'll get a permission denied page
        raise PermissionDenied()

    def clean_username(self, username):
        return username


class CleanEmailUsernameMixin(object):
    """
    A RemoteUserLoginView mixin which implements ``clean_username()``
    to return the local part of a username which contains an email
    address.
    """

    def clean_username(self, username):
        """
        Return just the local part of the email. This will be the CRSID
        when used with Shibboleth for Cambridge users.

        For example::

            clean_username("foo@example.com") => "foo"
        """
        return username.split("@")[0]


class ShibbolethRemoteUserLoginView(
        CleanEmailUsernameMixin, RemoteUserLoginView):
    """
    A RemoteUserLoginView subclass which uses just the local part of the
    full shib email ``REMOTE_USER`` value as the username.

    For example, shib might provide ``mrbob@example.com`` as the
    ``REMOTE_USER`` value. We'd use ``mrbob`` as the username.

    This is useful when compatability with Raven is desired. i.e. just
    CRSID rather than CRSID@cam.ac.uk usernames.

    This should not be used if shib is to be used with users from
    multiple domains, otherwise usernames could collide.
    """


remote_user_login_view = ShibbolethRemoteUserLoginView.as_view()
