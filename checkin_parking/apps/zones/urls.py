"""
.. module:: checkin_parking.apps.zones.urls
   :synopsis: Checkin Parking Reservation Zone URLs.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ...urls import administrative_access
from .ajax import update_buildings, delete_zone
from .views import ZoneListView, ZoneCreateView, ZoneUpdateView

app_name = 'zones'

urlpatterns = [
    url(r'^list/$', login_required(administrative_access(ZoneListView.as_view())), name='list_zones'),
    url(r'^create/$', login_required(administrative_access(ZoneCreateView.as_view())), name='create_zone'),
    url(r'^update/(?P<id>\d+)/$', login_required(administrative_access(ZoneUpdateView.as_view())), name='update_zone'),
    url(r'^ajax/delete/$', login_required(administrative_access(delete_zone)), name='delete_zone'),
    url(r'^ajax/update_buildings/$', login_required(update_buildings), name='ajax_update_building'),
]
