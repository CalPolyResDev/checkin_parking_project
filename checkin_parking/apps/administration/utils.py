"""
.. module:: checkin_parking.apps.administration.utils
   :synopsis: Checkin Parking Reservation Administration Utilities.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from collections import namedtuple

from django.db import connection, connections, transaction

from rmsconnector.exceptions import UnsupportedCommunityException
from rmsconnector.models import RoomBooking
from rmsconnector.utils import get_current_term, Resident

from ..administration.models import AdminSettings
from ..zones.models import Building, Community
from ..core.models import CheckinParkingUser


def namedtuplefetchall(cursor):
    """
    Return all rows from a cursor as a namedtuple.
    https://docs.djangoproject.com/en/1.9/topics/db/sql/#executing-custom-sql-directly
    """

    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def sync_zone_data():
    with transaction.atomic():
        cursor = connection.cursor()
        
        # Purge Building and Community Data
        Building.objects.all().delete()
        Community.objects.all().delete()

        # Grab buildings and communities from master and copy to slave
        cursor.execute("INSERT INTO checkin_parking.zones_community SELECT * FROM resnet_internal.core_community")
        cursor.execute("INSERT INTO checkin_parking.zones_building SELECT * FROM resnet_internal.core_building")

        # Add the open zone Feature
        open_community = Community.objects.create(name="All")
        Building.objects.create(name="All", community=open_community)

def sync_user_data():
    with transaction.atomic():
        # Purge User Data
        CheckinParkingUser.objects.all().delete()

        # Grab user data from RMS and copy to DB
        room_bookings = RoomBooking.objects.filter(term__term_id__icontains=get_current_term(), check_out=None)
        residents = []
        for room_booking in room_bookings:
            try:
                residents.append(Resident(room_booking=room_booking))
            except UnsupportedCommunityException:
                pass
            except AttributeError:
                logger.exception(room_booking)

        logger.debug("Sync Users: Exporting residents. Initiating data migration.")

        # Write data to DB
        admin_settings = AdminSettings.objects.get_settings()
        for resident in residents:
            CheckinParkingUser.objects.create(username=resident.principal_name, 
                                              first_name=resident.first_name, 
                                              last_name=resident.last_name, 
                                              full_name=resident.first_name + " " + resident.last_name, 
                                              email=resident.principal_name,
                                              building=Building.objects.get(name=resident.address_dict['building'].replace('_', ' '), community__name=resident.address_dict['community']) if resident.address_dict['building'] else None,
                                              term_type=resident.application_term_type(application_term=admin_settings.application_term, application_year=admin_settings.application_year),
                                              out_of_state=None,)

        logger.debug("Sync Users: Export of residents completed successfully.")
