"""
.. module:: checkin_parking.apps.administration.admin
   :synopsis: Checkin Parking Reservation Administration Admin Configuration.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib import admin

from .models import AdminSettings


class AdminSettingsManager(admin.ModelAdmin):
    list_display = ["reservation_open", "term_code", "timeslot_length"]


admin.site.register(AdminSettings, AdminSettingsManager)
