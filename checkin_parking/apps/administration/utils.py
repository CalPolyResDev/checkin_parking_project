"""
.. module:: checkin_parking.apps.administration.utils
   :synopsis: Checkin Parking Reservation Administration Utilities.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.db import connection, transaction

from ..zones.models import Building, Community


def sync_zone_data():
    cursor = connection.cursor()

    # Purge Building and Community Data
    Building.objects.all().delete()
    Community.objects.all().delete()

    # Copy data from master to slave
    cursor.execute("INSERT INTO checkin_parking.zones_community SELECT * FROM resnet_internal.core_community")
    cursor.execute("INSERT INTO checkin_parking.zones_building SELECT * FROM resnet_internal.core_building")

    transaction.commit_unless_managed()
