"""
.. module:: checkin_parking.apps.administration.admin
   :synopsis: Checkin Parking Reservation Administration Admin Configuration.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.contrib import admin

from .models import AdminSettings


class AdminSettingsManager(admin.ModelAdmin):
    list_display = ["reservation_open", "term_code", "timeslot_length", "application_year", "application_term"]


admin.site.register(AdminSettings, AdminSettingsManager)
