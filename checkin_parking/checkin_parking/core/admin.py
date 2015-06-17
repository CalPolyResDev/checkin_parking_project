from django.contrib import admin

from .models import CheckinParkingUser


class CheckinParkingUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_ral_manager', 'is_developer', 'reservation', )
    list_filter = ('is_ral_manager', 'is_developer')


admin.site.register(CheckinParkingUser, CheckinParkingUserAdmin)
