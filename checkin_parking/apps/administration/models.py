"""
.. module:: checkin_parking.apps.administration.models
   :synopsis: Checkin Parking Reservation Administration Models.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""
from datetime import date, datetime


from django.db.models.base import Model
from django.db.models.fields import PositiveSmallIntegerField, CharField, DateField
from django.utils import timezone

from .managers import AdminSettingsManager
from django.utils.functional import cached_property


class AdminSettings(Model):
    """Administrative settings."""
    APPLICATION_TERMS_CHOICES = [('FA', 'Fall'),
                                 ('WI', 'Winter'),
                                 ('SP', 'Spring'),
                                 ('SU', 'Summer')]

    term_code = PositiveSmallIntegerField(default=2178, verbose_name='Term Code')
    application_term = CharField(default=APPLICATION_TERMS_CHOICES[0][0], choices=APPLICATION_TERMS_CHOICES, max_length=2)
    application_year = PositiveSmallIntegerField(default=datetime.now().year)
    timeslot_length = PositiveSmallIntegerField(default=40, verbose_name='Time Slot Length (in Minutes)')
    reservation_close_day = DateField(default=timezone.now)

    objects = AdminSettingsManager()

    @cached_property
    def reservation_open(self):
        return date.today() <= self.reservation_close_day

    class Meta:
        verbose_name = "Admin Settings"
        verbose_name_plural = "Admin Settings"
