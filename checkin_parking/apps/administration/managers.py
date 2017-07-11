"""
.. module:: checkin_parking.apps.core.managers
   :synopsis: Checkin Parking Reservation Core Managers.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.db.models.manager import Manager


class AdminSettingsManager(Manager):

    def get_settings(self):
        settings, created = self.get_queryset().get_or_create(id=1)
        return settings
