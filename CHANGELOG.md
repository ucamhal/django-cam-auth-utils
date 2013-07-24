django_cam_auth_utils Changelog
===============================


0.0.2 - 2013-07-24
------------------
* Fixed `RemoteUserLoginView` throwing an exception when no next param was
  provided.
* Prevented `RemoteUserLoginView`'s redirect responses from being cached.
  Previously they were 301, they're now 302 redirects with appropriate
  `Cache-Control` headers.
* Added __version__ and __version_info__ params to `django_cam_auth_utils`
  module.


0.0.1 - 2013-06-13
------------------
* Initial release
