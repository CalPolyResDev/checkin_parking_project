"""
.. module:: checkin_parking.zones.models
   :synopsis: Checkin Parking Reservation Zone Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.db.models.base import Model
from django.db.models.fields import PositiveSmallIntegerField, CharField
from django.db.models.fields.related import ForeignKey, ManyToManyField


class Community(Model):
    """Housing Community."""

    name = CharField(max_length=30, verbose_name="Community Name")

    def __unicode__(self):
        return self.name


class Building(Model):
    """Housing Building."""

    name = CharField(max_length=30, verbose_name="Building Name")
    community = ForeignKey(Community, verbose_name="Community")

    def __unicode__(self):
        return str(self.community) + " " + self.name


class Zone(Model):
    """A Parking zone."""

    number = PositiveSmallIntegerField(verbose_name="Zone Number")
    community = ForeignKey(Community, verbose_name="Community")
    buildings = ManyToManyField(Building, verbose_name="Building(s)")

    def __unicode__(self):
        return str(self.community) + " " + str(self.number)

    def _get_building_list(self):
        return [building.name for building in self.buildings.all()]
    building_list = property(_get_building_list)

    class Meta:
        unique_together = ('number', 'community')
