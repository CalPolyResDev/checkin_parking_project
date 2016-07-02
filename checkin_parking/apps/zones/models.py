"""
.. module:: checkin_parking.zones.models
   :synopsis: Checkin Parking Reservation Zone Models.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.db.models.base import Model
from django.db.models.fields import PositiveSmallIntegerField, CharField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.utils.functional import cached_property


class Community(Model):
    """Housing Community."""

    name = CharField(max_length=30, verbose_name="Community Name")

    def __str__(self):
        return self.name


class Building(Model):
    """Housing Building."""

    name = CharField(max_length=30, verbose_name="Building Name")
    community = ForeignKey(Community, verbose_name="Community", related_name="buildings")

    def __str__(self):
        return self.name


class Zone(Model):
    """A Parking zone."""

    name = CharField(max_length=30, unique=True, verbose_name="Name")
    community = ForeignKey(Community, verbose_name="Community")
    buildings = ManyToManyField(Building, verbose_name="Building(s)")
    capacity = PositiveSmallIntegerField(default=30, verbose_name="Capacity")

    @property
    def formatted_building_list(self):
        return ", ".join(self.building_list)

    @cached_property
    def building_list(self):
        return [building.name for building in self.buildings.all().order_by("name")]

    def __str__(self):
        return self.name
