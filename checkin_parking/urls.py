"""
.. module:: checkin_parking.urls
   :synopsis: Checkin Parking Reservation URLs.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: RJ Almada <almada.dev@gmail.com>

"""

import logging

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static as static_url
from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import PermissionDenied
from django.views.defaults import server_error, permission_denied, page_not_found
from django.views.generic import TemplateView, RedirectView
from django_cas_ng.views import login as auth_login, logout as auth_logout

from .apps.core.views import IndexView
from .apps.pdfs.views import ParkingPassPDFView
from .apps.zones.ajax import update_building
from .apps.zones.views import ZoneCreateView


def permissions_check(test_func, raise_exception=True):
    """
    Decorator for views that checks whether a user has permission to view the
    requested page, redirecting to the log-in page if neccesary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.

    :param test_func: A callable test that takes a User object and returns true if the test passes.
    :type test_func: callable
    :param raise_exception: Determines whether or not to throw an exception when permissions test fails.
    :type raise_exception: bool

    """

    def check_perms(user):
        # First check if the user has the permission (even anon users)
        if test_func(user):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms)

administration_access = permissions_check((lambda user: user.is_admin))

admin.autodiscover()

logger = logging.getLogger(__name__)


# Core
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^login/$', auth_login, name='login'),
    url(r'^logout/$', auth_logout, name='logout'),  # kwargs={'next_page': settings.CAS_LOGOUT_URL},
    url(r'^favicon\.ico$', RedirectView.as_view(url=static('images/icons/favicon.ico')), name='favicon'),
    url(r'^admin/', TemplateView.as_view(template_name="honeypot.html"), name="honeypot"),  # admin site urls, honeypot
    url(r'^flugzeug/', include(admin.site.urls)),  # admin site urls, masked
]

# Sessions
urlpatterns += [
    url(r'^sessions/list/$', login_required(administration_access(IndexView.as_view())), name='list_sessions'),
    url(r'^sessions/create/$', login_required(administration_access(IndexView.as_view())), name='create_sessions'),
    url(r'^sessions/(?P<id>\d+)/$', login_required(administration_access(IndexView.as_view())), name='edit_session'),
    url(r'^sessions/(?P<id>\d+)/delete/$', login_required(administration_access(IndexView.as_view())), name='delete_session'),
    url(r'^sessions/reservation/reserve/$', login_required(IndexView.as_view()), name='reserve_session'),
    url(r'^sessions/reservation/detail/$', login_required(IndexView.as_view()), name='view_reservation'),
    url(r'^sessions/reservation/change/$', login_required(IndexView.as_view()), name='change_reservation'),
    url(r'^sessions/reservation/cancel/$', login_required(IndexView.as_view()), name='cancel_reservation'),
    url(r'^sessions/update/$', login_required(IndexView.as_view()), name='update_sessions'),
]

# Zones
urlpatterns += [
    url(r'^zones/list/$', login_required(administration_access(IndexView.as_view())), name='list_zones'),
    url(r'^zones/create/$', login_required(administration_access(ZoneCreateView.as_view())), name='create_zone'),
    url(r'^zones/(?P<id>\d+)/$', login_required(administration_access(IndexView.as_view())), name='edit_zone'),
    url(r'^zones/(?P<id>\d+)/delete/$', login_required(administration_access(IndexView.as_view())), name='delete_zone'),
    url(r'^zones/ajax/update_building/$', login_required(update_building), name='ajax_update_building'),
]

# PDFs
urlpatterns += [
    url(r'^pdfs/maps/list/$', login_required(administration_access(IndexView.as_view())), name='list_maps'),
    url(r'^pdfs/parking_pass/generate/$', login_required(ParkingPassPDFView.as_view()), name='generate_parking_pass'),
]

# Residents
urlpatterns += [
    url(r'^residents/lookup/$', login_required(administration_access(IndexView.as_view())), name='lookup_residents'),
]

# Statistics
urlpatterns += [
    url(r'^statistics/$', login_required(administration_access(IndexView.as_view())), name='statistics'),
]

# Administration
urlpatterns += [
    url(r'^admin/settings/$', login_required(administration_access(IndexView.as_view())), name='settings'),
    url(r'^admin/purge/$', login_required(administration_access(IndexView.as_view())), name='purge'),
]

# Raise errors on purpose
urlpatterns += [
    url(r'^500/$', server_error),
    url(r'^403/$', permission_denied),
    url(r'^404/$', page_not_found),
]

if settings.DEBUG:
    urlpatterns += static_url(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
