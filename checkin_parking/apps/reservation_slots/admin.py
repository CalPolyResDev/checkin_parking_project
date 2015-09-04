from django.contrib import admin

from .models import ReservationSlot


class SessionAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'zone', 'class_level', 'duration')

admin.site.register(ReservationSlot, SessionAdmin)
