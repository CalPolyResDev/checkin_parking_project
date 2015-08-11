from django.contrib import admin

from .models import AdminSettings

admin.site.register(AdminSettings, admin.ModelAdmin)
