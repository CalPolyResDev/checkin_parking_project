from django.contrib import admin

from .models import Zone


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('number', 'community', 'buildings', )

admin.site.register(Zone, ZoneAdmin)
