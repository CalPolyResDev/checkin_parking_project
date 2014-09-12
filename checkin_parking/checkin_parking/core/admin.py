from django.contrib import admin

from .models import Community, Building, CheckinParkingUser


class CheckinParkingUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_ral_manager', 'is_developer')
    list_filter = ('is_ral_manager', 'is_developer')


admin.site.register(Community, admin.ModelAdmin)
admin.site.register(Building, admin.ModelAdmin)
admin.site.register(CheckinParkingUser, CheckinParkingUserAdmin)
