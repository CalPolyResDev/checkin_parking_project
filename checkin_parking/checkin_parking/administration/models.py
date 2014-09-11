"""
.. module:: checkin_parking.administration.models
   :synopsis: Checkin Parking Reservation Administration Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: RJ Almada <robert.j.almada@gmail.com>

"""

from django.db.models.base import Model
from django.db.models.fields import BooleanField, IntegerField


class AdminSettings(Model):
    """ Administrative settings."""

    reservation_open = BooleanField(default=True, verbose_name=u'Reservation Status')
    term_code = IntegerField(max_length=4, verbose_name=u'Term Code')