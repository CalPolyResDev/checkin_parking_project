"""
.. module:: checkin_parking.checkin_sessions.models
   :synopsis: Checkin Parking Reservation Session Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from datetime import datetime

from django.db.models.base import Model
from django.db.models.fields import DateField, TimeField, PositiveSmallIntegerField, SmallIntegerField
from django.db.models.fields.related import ForeignKey

from ..zones.models import Zone


class Session(Model):
    """ A parking session."""

    CLASS_LEVELS = ['Freshman', 'Transfer', 'Continuing', 'All']
    CLASS_LEVEL_CHOICES = [(CLASS_LEVELS.index(class_level), class_level) for class_level in CLASS_LEVELS]

    date = DateField(verbose_name="Date")
    time = TimeField(verbose_name="Time")
    zone = ForeignKey(Zone, verbose_name="Zone")
    class_level = SmallIntegerField(default=CLASS_LEVELS.index('All'), choices=CLASS_LEVEL_CHOICES, verbose_name='Class Level')
    duration = PositiveSmallIntegerField(default=40, verbose_name="Duration (Minutes)")
    capacity = PositiveSmallIntegerField(default=30, verbose_name="Capacity")

    def _get_datetime(self):
        combined = datetime.combine(self.date, self.time)
        return datetime.strftime(combined, "%A, %B %d, %Y %I:%M%p")  # Format: Monday, January 01, 2012 08:00am
    datetime = property(_get_datetime)

    def __unicode__(self):
        return self._get_datetime()
