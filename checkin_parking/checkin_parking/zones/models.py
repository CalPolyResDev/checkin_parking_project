"""
.. module:: checkin_parking.zones.models
   :synopsis: Checkin Parking Reservation Zone Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""
from django.db.models.base import Model
from django.db.models.fields import PositiveSmallIntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from ..core.models import Community, Building


class Zone(Model):
    """A Parking zone."""

    number = PositiveSmallIntegerField(verbose_name="Zone Number")
    community = ForeignKey(Community, verbose_name="Community")
    buildings = ManyToManyField(Building, verbose_name="Buildings")

    def __unicode__(self):
        return str(self.community) + " " + str(self.number)

    class Meta:
        unique_together = ('number', 'community')