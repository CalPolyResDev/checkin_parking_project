"""
.. module:: checkin_parking.apps.administration.models
   :synopsis: Checkin Parking Reservation Administration Models.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""
from datetime import datetime


from django.db.models.base import Model
from django.db.models.fields import BooleanField, PositiveSmallIntegerField, CharField

from rmsconnector.utils import get_current_term

from .managers import AdminSettingsManager


class AdminSettings(Model):
    """Administrative settings."""
    APPLICATION_TERMS_CHOICES = [('FA', 'Fall'),
                                 ('WI', 'Winter'),
                                 ('SP', 'Spring'),
                                 ('SU', 'Summer')]

    reservation_open = BooleanField(default=True, verbose_name='Reservation Open')
    term_code = PositiveSmallIntegerField(default=get_current_term(), verbose_name='Term Code')
    application_term = CharField(default=APPLICATION_TERMS_CHOICES[0][0], choices=APPLICATION_TERMS_CHOICES, max_length=2)
    application_year = PositiveSmallIntegerField(default=datetime.now().year)
    timeslot_length = PositiveSmallIntegerField(default=40, verbose_name='Time Slot Length (in Minutes)')

    objects = AdminSettingsManager()

    class Meta:
        verbose_name = "Admin Settings"
        verbose_name_plural = "Admin Settings"
