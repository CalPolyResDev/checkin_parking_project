"""
.. module:: checkin_parking.urls
   :synopsis: Checkin Parking Reservation URLs.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>
.. moduleauthor:: Thomas Willson <thomas.willson@me.com>

"""

import logging

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static as static_url
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group as group_unregistered
from django.core.exceptions import PermissionDenied
from django.views.defaults import permission_denied, page_not_found
from django.views.generic import TemplateView

<<<<<<< HEAD
from .apps.administration.ajax import purge
from .apps.administration.views import AdminSettingsUpdateView, PurgeView, PDFMapUploadView, BecomeStudentView
from .apps.core.views import IndexView, handler500
from .apps.reservations.ajax import reserve_slot, cancel_reservation, delete_timeslot
from .apps.reservations.views import GenerateReservationSlotsView, ParkingPassPDFView, ParkingPassVerificationView, ReserveView, ViewReservationView, ChangeReservationView, TimeSlotListView
from .apps.zones.ajax import BuildingChainedAjaxView, delete_zone
from .apps.zones.views import ZoneListView, ZoneCreateView, ZoneUpdateView
=======
from .apps.core.views import handler500
from .settings.base import MAIN_APP_NAME
>>>>>>> 162fb0838f7a0655298cf54f72052efb0d241eae


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

administrative_access = permissions_check((lambda user: user.is_admin))

admin.autodiscover()
admin.site.unregister(group_unregistered)

logger = logging.getLogger(__name__)

handler500 = handler500


urlpatterns = [
    url(r'^admin/', TemplateView.as_view(template_name="honeypot.djhtml"), name="honeypot"),  # admin site urls, honeypot
    url(r'^flugzeug/', include(admin.site.urls)),  # admin site urls, masked
    url(r'^reservations/', include(MAIN_APP_NAME + '.apps.reservations.urls')),
    url(r'^zones/', include(MAIN_APP_NAME + '.apps.zones.urls')),
    url(r'^statistics/', include(MAIN_APP_NAME + '.apps.statistics.urls')),
    url(r'^settings/', include(MAIN_APP_NAME + '.apps.administration.urls')),
    url(r'^', include(MAIN_APP_NAME + '.apps.core.urls')),
]

# Raise errors on purpose
urlpatterns += [
    url(r'^500/$', handler500),
    url(r'^403/$', permission_denied),
    url(r'^404/$', page_not_found),
]

if settings.DEBUG:
    urlpatterns += static_url(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
