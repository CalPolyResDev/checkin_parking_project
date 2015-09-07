"""
.. module:: checkin_parking.apps.core.admin
   :synopsis: Checkin Parking Reservation Core Admin Configuration.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib import admin

from .models import CheckinParkingUser


class CheckinParkingUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_admin', 'is_superuser', 'reservation']
    list_filter = ['is_admin', 'is_superuser']
    search_fields = ['username']


admin.site.register(CheckinParkingUser, CheckinParkingUserAdmin)
