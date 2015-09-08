"""
.. module:: checkin_parking.checkin_sessions.models
   :synopsis: Checkin Parking Reservation Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from datetime import datetime

from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields import DateField, TimeField, PositiveSmallIntegerField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.utils.functional import cached_property

from ..core.managers import DefaultRelatedManager
from ..core.models import CheckinParkingUser
from ..zones.models import Zone


CLASS_LEVELS = ['Freshman', 'Transfer', 'Continuing', 'All']
CLASS_LEVEL_CHOICES = [(CLASS_LEVELS.index(class_level), class_level) for class_level in CLASS_LEVELS]


class TimeSlot(Model):
    """A slot of time."""

    date = DateField(verbose_name="Date")
    time = TimeField(verbose_name="Time")
    term_code = PositiveSmallIntegerField(verbose_name="Term Code")

    @cached_property
    def datetime(self):
        combined = datetime.combine(self.date, self.time)
        return datetime.strftime(combined, settings.PYTHON_DATETIME_FORMAT)

    def __str__(self):
        return self.datetime + " (" + str(self.term) + ")"


class ReservationSlot(Model):
    """ A parking session."""

    class_level = PositiveSmallIntegerField(default=CLASS_LEVELS.index('All'), choices=CLASS_LEVEL_CHOICES, verbose_name='Class Level')
    timeslot = ForeignKey(TimeSlot, related_name="reservationslots", verbose_name="Time Slot")
    zone = ForeignKey(Zone, related_name="reservationslots", verbose_name="Zone")
    resident = OneToOneField(CheckinParkingUser, null=True, blank=True, related_name="reservationslot", verbose_name="Resident", on_delete=SET_NULL)

    objects = DefaultRelatedManager(select_related=["timeslot", "zone", "resident"])

    def __str__(self):
        return str(self.timeslot) + " - " + str(self.zone) + ": " + str(self.resident) if self.resident else "Open"
