from django.contrib import admin

from .models import Zone


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('number', 'community', 'building_list')

admin.site.register(Zone, ZoneAdmin)
