"""
.. module:: checkin_parking.apps.core.managers
   :synopsis: Checkin Parking Reservation Core Managers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.db.models.manager import Manager


class AdminSettingsManager(Manager):

    def get_settings(self):
        return self.get_queryset().get_or_create(id=1)
