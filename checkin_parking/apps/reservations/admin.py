"""
.. module:: checkin_parking.apps.reservations.admin
   :synopsis: Checkin Parking Reservation Reservation Admin Configuration.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.contrib import admin

from .models import TimeSlot, ReservationSlot


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'term_code']
    list_filter = ['term_code']


class ReservationSlotAdmin(admin.ModelAdmin):
    list_display = ['class_level', 'out_of_state', 'assisted_move_in', 'timeslot', 'zone', 'resident']
    list_filter = ['zone', 'class_level', 'out_of_state', 'assisted_move_in', 'timeslot']


admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(ReservationSlot, ReservationSlotAdmin)
