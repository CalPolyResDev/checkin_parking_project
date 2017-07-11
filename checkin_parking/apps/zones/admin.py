"""
.. module:: checkin_parking.apps.zones.admin
   :synopsis: Checkin Parking Reservation Zone Admin Configuration.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.contrib import admin

from .models import Zone


class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'community', 'building_list', 'capacity']

admin.site.register(Zone, ZoneAdmin)
