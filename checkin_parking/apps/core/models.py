"""
.. module:: checkin_parking.apps.core.models
   :synopsis: Checkin Parking Reservation Core Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db.models.fields import CharField, EmailField, BooleanField
from django.db.models.fields.related import ForeignKey
from django.db.models.deletion import SET_NULL
from django.utils import timezone
from django.utils.functional import cached_property
from django.core.mail import send_mail


class CheckinParkingUserManager(UserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()

        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, **extra_fields)
        user.set_password("!")
        user.save(using=self._db)

        return user


class CheckinParkingUser(AbstractBaseUser, PermissionsMixin):
    """Checkin Parking Reservation User Model"""

    username = CharField(max_length=30, unique=True, verbose_name='Principal Name')
    first_name = CharField(max_length=30, blank=True, verbose_name='First Name')
    last_name = CharField(max_length=30, blank=True, verbose_name='Last Name')
    full_name = CharField(max_length=30, blank=True, verbose_name='Full Name')
    email = EmailField(blank=True, verbose_name='Email Address')

    # Session reservation
    reservation = ForeignKey('checkin_sessions.Session', null=True, blank=True, default=None, on_delete=SET_NULL)

    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_admin = BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = CheckinParkingUserManager()

    class Meta:
        verbose_name = 'Checkin Parking Reservation User'

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.first_name

    @cached_property
    def dn(self):
        return "CN=" + self.username.split("@", 1)[0] + "," + settings.LDAP_GROUPS_USER_BASE_DN

    def email_user(self, subject, message, from_email=None):
        """Sends an email to this user."""

        if self.email:
            send_mail(subject, message, from_email, [self.email])
