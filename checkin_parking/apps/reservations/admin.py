"""
.. module:: checkin_parking.apps.reservations.admin
   :synopsis: Checkin Parking Reservation Reservation Admin Configuration.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib import admin

from .models import TimeSlot, ReservationSlot


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'term']
    list_filter = ['term']


class ReservationSlotAdmin(admin.ModelAdmin):
    list_display = ['class_level', 'timeslot', 'zone', 'resident']
    list_filter = ['zone', 'class_level', 'timeslot']


admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(ReservationSlot, ReservationSlotAdmin)
