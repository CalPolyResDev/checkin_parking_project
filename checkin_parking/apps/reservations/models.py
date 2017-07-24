"""
.. module:: checkin_parking.checkin_sessions.models
   :synopsis: Checkin Parking Reservation Models.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from datetime import datetime, timedelta

from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields import CharField, DateField, TimeField, PositiveSmallIntegerField, BooleanField, DateTimeField, NullBooleanField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.utils.functional import cached_property

from rmsconnector.constants import FRESHMAN, TRANSFER, CONTINUING

from ..administration.models import AdminSettings
from ..core.managers import DefaultRelatedManager
from ..core.models import CheckinParkingUser
from ..zones.models import Zone


CLASS_LEVELS = [FRESHMAN, TRANSFER, CONTINUING,
                FRESHMAN + '/' + TRANSFER, FRESHMAN + '/' + CONTINUING, TRANSFER + '/' + CONTINUING,
                FRESHMAN + '/' + TRANSFER + '/' + CONTINUING]
CLASS_LEVEL_CHOICES = [(class_level, class_level) for class_level in CLASS_LEVELS]


class TimeSlot(Model):
    """A slot of time."""

    date = DateField(verbose_name="Date")
    time = TimeField(verbose_name="Time")
    assisted_move_in = BooleanField(default=False, verbose_name="Assisted Move In?")
    term_code = PositiveSmallIntegerField(verbose_name="Term Code")

    @cached_property
    def datetime(self):
        combined = datetime.combine(self.date, self.time)
        return datetime.strftime(combined, settings.PYTHON_DATETIME_FORMAT)

    @cached_property
    def datetime_obj(self):
        combined = datetime.combine(self.date, self.time)
        return combined

    @cached_property
    def end_time(self):
        return (datetime.combine(datetime.today(), self.time) + timedelta(minutes=AdminSettings.objects.get_settings().timeslot_length)).time()

    @cached_property
    def end_datetime_obj(self):
        combined = datetime.combine(self.date, self.time)
        combined += timedelta(minutes=AdminSettings.objects.get_settings().timeslot_length)
        return combined

    def __str__(self):
        return self.datetime + " (" + str(self.term_code) + ")"


class ReservationSlot(Model):
    """ A parking session."""

    class_level = CharField(max_length=30, default=CLASS_LEVELS.index(FRESHMAN + '/' + TRANSFER + '/' + CONTINUING), choices=CLASS_LEVEL_CHOICES, verbose_name="Class Level")
    out_of_state = BooleanField(default=False, verbose_name="In State?")
    timeslot = ForeignKey(TimeSlot, related_name="reservationslots", verbose_name="Time Slot")
    zone = ForeignKey(Zone, related_name="reservationslots", verbose_name="Zone")
    resident = OneToOneField(CheckinParkingUser, null=True, blank=True, related_name="reservationslot", verbose_name="Resident", on_delete=SET_NULL)

    objects = DefaultRelatedManager(select_related=["timeslot", "zone", "resident"])

    last_scanned = DateTimeField(null=True, blank=True)
    last_scanned_on_time = NullBooleanField()

    def __str__(self):
        return str(self.timeslot) + " - " + str(self.zone) + ": " + (str(self.resident) if self.resident else "Open")
