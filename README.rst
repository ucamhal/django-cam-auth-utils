django-cam-auth-utils
=====================

This package contains a Django app which provides interoperability with
Raven/Shib authentication systems @ Cambridge University.


django_cam_auth_utils.views.RemoteUserLoginView
-----------------------------------------------

This view class provides an alternative to RemoteUserMiddleware for the
use case in which a single URL (e.g. /accounts/login) is protected by
Raven/Shib etc.


django_cam_auth_utils.admin.RemoteUserLoginView
-----------------------------------------------