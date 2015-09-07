"""
.. module:: checkin_parking.urls
   :synopsis: Checkin Parking Reservation URLs.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Thomas Willson <thomas.willson@me.com>

"""

import logging

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static as static_url
from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group as group_unregistered
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import PermissionDenied
from django.views.defaults import permission_denied, page_not_found
from django.views.generic import TemplateView, RedirectView
from django_cas_ng.views import login as auth_login, logout as auth_logout

from .apps.administration.views import AdminSettingsUpdateView
from .apps.core.views import IndexView, handler500
from .apps.pdfs.views import ParkingPassPDFView, ParkingPassVerificationView
from .apps.zones.ajax import update_buildings, delete_zone
from .apps.zones.views import ZoneListView, ZoneCreateView, ZoneUpdateView


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


# Core
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^login/$', auth_login, name='login'),
    url(r'^logout/$', auth_logout, name='logout'),  # kwargs={'next_page': settings.CAS_LOGOUT_URL},
    url(r'^favicon\.ico$', RedirectView.as_view(url=static('images/icons/favicon.ico')), name='favicon'),
    url(r'^admin/', TemplateView.as_view(template_name="honeypot.html"), name="honeypot"),  # admin site urls, honeypot
    url(r'^flugzeug/', include(admin.site.urls)),  # admin site urls, masked
]

# Reservations
urlpatterns += [
    url(r'^reservations/slots/generate/$', login_required(administrative_access(IndexView.as_view())), name='generate_reservation_slots'),

    url(r'^reservations/slots/list/$', login_required(administrative_access(IndexView.as_view())), name='list_time_slots'),
    url(r'^reservations/slots/(?P<id>\d+)/$', login_required(administrative_access(IndexView.as_view())), name='update_time_slot'),
    url(r'^reservations/slots/(?P<id>\d+)/delete/$', login_required(administrative_access(IndexView.as_view())), name='delete_time_slot'),

    url(r'^reservations/reserve/$', login_required(IndexView.as_view()), name='reserve'),
    url(r'^reservations/view/$', login_required(IndexView.as_view()), name='view_reservation'),
    url(r'^reservations/change/$', login_required(IndexView.as_view()), name='change_reservation'),
    url(r'^reservations/cancel/$', login_required(IndexView.as_view()), name='cancel_reservation'),
]

# Zones
urlpatterns += [
    url(r'^zones/list/$', login_required(administrative_access(ZoneListView.as_view())), name='list_zones'),
    url(r'^zones/create/$', login_required(administrative_access(ZoneCreateView.as_view())), name='create_zone'),
    url(r'^zones/update/(?P<id>\d+)/$', login_required(administrative_access(ZoneUpdateView.as_view())), name='update_zone'),
    url(r'^zones/ajax/delete/$', login_required(administrative_access(delete_zone)), name='delete_zone'),
    url(r'^zones/ajax/update_buildings/$', login_required(update_buildings), name='ajax_update_building'),
]

# PDFs
urlpatterns += [
    url(r'^pdfs/maps/list/$', login_required(administrative_access(IndexView.as_view())), name='list_maps'),
    url(r'^pdfs/parking-pass/generate/(?P<reservation_id>\d+)/$', login_required(ParkingPassPDFView.as_view()), name='generate_parking_pass'),
    url(r'^pdfs/parking-pass/verify/(?P<reservation_id>\d+)/(?P<user_id>\d+)/$', ParkingPassVerificationView.as_view(), name='verify_parking_pass'),
]

# Statistics
urlpatterns += [
    url(r'^statistics/$', login_required(administrative_access(IndexView.as_view())), name='statistics'),
]

# Administration
urlpatterns += [
    url(r'^settings/$', login_required(administrative_access(AdminSettingsUpdateView.as_view())), name='settings'),
    url(r'^settings/purge/$', login_required(administrative_access(IndexView.as_view())), name='purge'),
]

# Raise errors on purpose
urlpatterns += [
    url(r'^500/$', handler500),
    url(r'^403/$', permission_denied),
    url(r'^404/$', page_not_found),
]

if settings.DEBUG:
    urlpatterns += static_url(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
