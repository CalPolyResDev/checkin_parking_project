"""
.. module:: checkin_parking.apps.core.tasks
   :synopsis: Checkin Parking Core Tasks

.. moduleauthor:: Thomas Willson <thomas.willson@icloud.com>

"""
from concurrent.futures import ThreadPoolExecutor

from rmsconnector.utils import Resident
from uwsgidecorators import cron

from ..administration.models import AdminSettings
from ..zones.models import Building
from .models import CheckinParkingUser


@cron(-3, -1, -1, -1, -1)
def update_users_buildings():
    def update_user_building(user):
        address_dict = Resident(principal_name=user.email, term_code=AdminSettings.objects.get_settings().term_code)

        if address_dict['building']:
            user.building = Building.objects.get(name=address_dict['building'], community__name=address_dict['community'])
            user.save()

    with ThreadPoolExecutor(max_workers=20) as pool:
        pool.map(update_user_building, CheckinParkingUser.objects.all())
