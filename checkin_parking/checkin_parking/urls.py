"""
.. module:: checkin_parking.urls
   :synopsis: Checkin Parking Reservation URLs.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: RJ Almada <almada.dev@gmail.com>

"""

import logging

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.core.exceptions import PermissionDenied
from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import RedirectView

from checkin_parking.settings.base import ral_manager_access_test
from .core.views import IndexView, LoginView, logout


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

ral_manager_access = permissions_check(ral_manager_access_test)

admin.autodiscover()

logger = logging.getLogger(__name__)


# Core
urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='%simages/icons/favicon.ico' % settings.STATIC_URL), name='favicon'),
    url(r'^flugzeug/', include(admin.site.urls)),  # admin site urls, masked
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
)

# Sessions
urlpatterns = patterns('',
    url(r'^sessions/list/$', login_required(), name='list_sessions'),
    url(r'^sessions/update/$', login_required(), name='update_sessions'),
    url(r'^sessions/create/$', login_required(ral_manager_access()), name='create_sessions'),
    url(r'^sessions/edit/$', login_required(ral_manager_access()), name='edit_session'),
    url(r'^sessions/delete/$', login_required(ral_manager_access()), name='delete_session'),
    url(r'^sessions/reservation/reserve/$', login_required(), name='reserve_session'),
    url(r'^sessions/reservation/detail/$', login_required(), name='view_reservation'),
    url(r'^sessions/reservation/change/$', login_required(), name='change_reservation'),
    url(r'^sessions/reservation/cancel/$', login_required(), name='cancel_reservation'),
)

# Zones
urlpatterns = patterns('',
    url(r'^zones/list/$', login_required(ral_manager_access()), name='list_zones'),
)

# PDFs
urlpatterns = patterns('',
    url(r'^pdfs/maps/list/$', login_required(ral_manager_access()), name='list_maps'),
    url(r'^pdfs/parking_pass/edit/$', login_required(ral_manager_access()), name='edit_parking_pass'),
    url(r'^pdfs/parking_pass/generate/$', login_required(), name='generate_parking_pass'),
)

# Residents
urlpatterns = patterns('',
    url(r'^residents/lookup/$', login_required(ral_manager_access()), name='lookup_residents'),
)

# Statistics
urlpatterns = patterns('',
    url(r'^statistics/$', login_required(ral_manager_access()), name='statistics'),
)

# Administration
urlpatterns = patterns('',
    url(r'^admin/settings/$', login_required(ral_manager_access()), name='settings'),
    url(r'^admin/purge/$', login_required(ral_manager_access()), name='purge'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
