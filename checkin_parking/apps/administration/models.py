"""
.. module:: checkin_parking.apps.administration.models
   :synopsis: Checkin Parking Reservation Administration Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.db.models.base import Model
from django.db.models.fields import BooleanField, PositiveSmallIntegerField

from rmsconnector.utils import get_current_term


class AdminSettings(Model):
    """Administrative settings."""

    reservation_open = BooleanField(default=True, verbose_name='Reservation Open')
    term_code = PositiveSmallIntegerField(default=get_current_term, verbose_name='Term Code')
    timeslot_length = PositiveSmallIntegerField(default=40, verbose_name='Time Slot Length (in Minutes)')

    class Meta:
        verbose_name = "Admin Settings"
        verbose_name_plural = "Admin Settings"
