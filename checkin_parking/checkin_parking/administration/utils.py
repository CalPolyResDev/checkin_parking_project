"""
.. module:: checkin_parking.administration.utils
   :synopsis: Checkin Parking Reservation Administration Utilities.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: RJ Almada <robert.j.almada@gmail.com>

"""

from django.db import connection, transaction

from ..zones.models import Building, Community


def sync_zone_data():
    cursor = connection.cursor()

    # Purge Building and Community Data
    Building.objects.all().delete()
    Community.objects.all().delete()

    # Copy data from master to slave
    cursor.execute("INSERT INTO checkin_parking.zones_community SELECT * FROM common.community")
    cursor.execute("INSERT INTO checkin_parking.zones_building SELECT * FROM common.building")

    transaction.commit_unless_managed()
