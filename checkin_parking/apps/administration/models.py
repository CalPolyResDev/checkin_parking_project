"""
.. module:: checkin_parking.administration.models
   :synopsis: Checkin Parking Reservation Administration Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: RJ Almada <robert.j.almada@gmail.com>

"""

from django.db.models.base import Model
from django.db.models.fields import BooleanField, IntegerField, \
    PositiveSmallIntegerField

from rmsconnector.utils import get_current_term


class AdminSettings(Model):
    """ Administrative settings."""

    reservation_open = BooleanField(default=True, verbose_name=u'Reservation Open')
    term_code = PositiveSmallIntegerField(default=get_current_term, verbose_name=u'Term Code')

    class Meta:
        verbose_name_plural = "AdminSettings"
