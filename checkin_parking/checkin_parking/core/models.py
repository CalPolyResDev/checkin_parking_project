"""
.. module:: checkin_parking.core.models
   :synopsis: Checkin Parking Reservation Core Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import re

from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db.models import CharField, EmailField, BooleanField
from django.utils.http import urlquote
from django.core.mail import send_mail


class CheckinParkingUser(AbstractBaseUser, PermissionsMixin):
    """Checkin Parking Reservation User Model"""

    username = CharField(max_length=30, unique=True, verbose_name=u'Username')
    first_name = CharField(max_length=30, blank=True, verbose_name=u'First Name')
    last_name = CharField(max_length=30, blank=True, verbose_name=u'Last Name')
    email = EmailField(blank=True, verbose_name=u'Email Address')

    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    #
    # A set of flags for each user that decides what the user can and cannot see.
    # Flags are determined by which tools a user needs to fill his/her job description.
    #
    is_ral_manager = BooleanField(default=False)  # access to administrative functions
    is_developer = BooleanField(default=False)  # full access

    class Meta:
        verbose_name = u'Checkin Parking Reservation User'

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """Returns the first_name combined with the last_name separated via space with the possible '- ADMIN' removed."""

        full_name = '%s %s' % (self.first_name, re.sub(r' - ADMIN', '', self.last_name))
        return full_name.strip()

    def get_alias(self):
        """Returns the username with the possible '-admin' removed."""

        return re.sub(r'-admin', '', self.username)

    def get_short_name(self):
        "Returns the short name for the user."

        return self.get_alias()

    def email_user(self, subject, message, from_email=None):
        """Sends an email to this user."""

        if self.email:
            send_mail(subject, message, from_email, [self.email])
