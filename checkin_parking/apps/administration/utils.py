"""
.. module:: checkin_parking.apps.administration.utils
   :synopsis: Checkin Parking Reservation Administration Utilities.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from collections import namedtuple

from django.db import connection, connections, transaction

from ..zones.models import Building, Community


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
        # Purge Building and Community Data
        Building.objects.all().delete()
        Community.objects.all().delete()

        # Grab buildings and communities from master and copy to slave
        with connections["uhin"].cursor() as uhin_cursor:
            uhin_cursor.execute("SELECT * from core_community")
            communities = namedtuplefetchall(uhin_cursor)

            for community in communities:
                Community.objects.create(id=community.id, name=community.name)

            uhin_cursor.execute("SELECT * from core_building")
            buildings = namedtuplefetchall(uhin_cursor)

            for building in buildings:
                Building.objects.create(id=building.id, name=building.name, community=Community.objects.get(id=building.community_id))

        # Add the open zone Feature
        open_community = Community.objects.create(name="All")
        Building.objects.create(name="All", community=open_community)
