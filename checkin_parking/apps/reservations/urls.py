"""
.. module:: checkin_parking.apps.reservations.urls
   :synopsis: Checkin Parking Reservation Reservations URLs.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ...urls import administrative_access
from ..core.views import IndexView
from .ajax import reserve_slot, cancel_reservation, delete_timeslot
from .views import GenerateReservationSlotsView, ParkingPassPDFView, ParkingPassVerificationView, ReserveView, ViewReservationView, ChangeReservationView, TimeSlotListView


app_name = 'reservations'

urlpatterns = [
    url(r'^slots/generate/$', login_required(administrative_access(GenerateReservationSlotsView.as_view())), name='generate_reservation_slots'),

    url(r'^slots/list/$', login_required(administrative_access(TimeSlotListView.as_view())), name='list_time_slots'),
    url(r'^slots/(?P<id>\d+)/$', login_required(administrative_access(IndexView.as_view())), name='update_time_slot'),  # What?
    url(r'^ajax/delete_time_slot/$', login_required(administrative_access(delete_timeslot)), name='delete_time_slot'),

    url(r'^reserve/$', login_required(ReserveView.as_view()), name='reserve'),
    url(r'^ajax/reserve_slot/$', login_required(reserve_slot), name='reserve_slot'),
    url(r'^view/$', login_required(ViewReservationView.as_view()), name='view_reservation'),
    url(r'^change/$', login_required(ChangeReservationView.as_view()), name='change_reservation'),
    url(r'^ajax/cancel/$', login_required(cancel_reservation), name='cancel_reservation'),

    url(r'^parking-pass/generate/$', login_required(ParkingPassPDFView.as_view()), name='generate_parking_pass'),
    url(r'^parking-pass/verify/(?P<reservation_id>\d+)/(?P<user_id>\d+)/$', ParkingPassVerificationView.as_view(), name='verify_parking_pass'),
]
