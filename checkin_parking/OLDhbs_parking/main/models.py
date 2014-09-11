from django.db.models import Model, CharField, TextField, IntegerField, DateField, TimeField, CommaSeparatedIntegerField, EmailField, BooleanField
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.mail import send_mail
from django.utils.http import urlquote

import re, datetime

#
# hbs_parking.main models
#
# Author: Alex Kavanaugh
# Email:  kavanaugh.development@outlook.com
# Author: Chase Voorhees
# Email:  chase@cjvoorhees.com
#


#
# Basic location model - usually corresponds to a building.
#     Multiple buildings may share the same zoneNum.
#
class Location(Model):
    key = CharField(max_length=30, primary_key=True, verbose_name=u'Name Key')
    name = CharField(max_length=30, verbose_name=u'Name')
    zoneNum = IntegerField(null=True, verbose_name=u'Zone Number')

    # Provides a human-readable representation of an object. In this case, the name of the location is returned.
    def __unicode__(self):
        return self.name

#
# A zone class, primarily used for dynamic PDF text generation based on zone number.
#
class Zone(Model):
    number = IntegerField(primary_key=True, verbose_name=u'Zone Number')
    text = TextField(verbose_name=u'Zone PDF Text')

    # Provides a human-readable representation of an object. In this case, the name of the location is returned.
    def __unicode__(self):
        return self.number

#
# Basic session class - can contain up to maxID rmsID's in the rmsID field
#     zone corresponds to zoneNum in the Location model.
#
class Session(Model):
    date = DateField(verbose_name=u'Date')
    time = TimeField(verbose_name=u'Time')
    maxID = IntegerField(default=25, verbose_name=u'Maximum Capacity')
    countID = IntegerField(default=0, verbose_name=u'Current Capacity')
    zone = IntegerField(default=0, verbose_name=u'Zone')

    # Use string.split(",", [maxsplit#]) to return list of split IDs
    rmsID = CommaSeparatedIntegerField(max_length=10000, verbose_name=u'Students')

    # Provides a human-readable representation of an object. In this case, the name of the location is returned.
    def __unicode__(self):
        dtCombination = datetime.datetime.combine(self.date, self.time)
        return datetime.datetime.strftime(dtCombination, "%A, %B %d, %Y %I:%M%p")  # Format: Monday, January 01, 2012 08:00am

#
# Statistics model - Instantiated and destroyed on use by utils_statistics.
# See utils_statistics.genCharts for corresponding chart usage
#
class AllDayAllLoc(Model):
    date = CharField(max_length=30, verbose_name=u'Date')
    numRegistered = IntegerField(default=0, verbose_name=u'Students Registered')
#
# Statistics model - Instantiated and destroyed on use by utils_statistics.
# See utils_statistics.genCharts for corresponding chart usage
#
class ByDaySepLoc(Model):
    date = CharField(max_length=30, verbose_name=u'Date')
    numRegistered = IntegerField(default=0, verbose_name=u'Students Registered')
    buildings = CharField(max_length=100, verbose_name=u'Location')
#
# Statistics model - Instantiated and destroyed on use by utils_statistics.
# See utils_statistics.genCharts for corresponding chart usage
#
class ByTimeAllLoc(Model):
    date = CharField(max_length=30, verbose_name=u'Date')
    time = CharField(max_length=30, verbose_name=u'Time')
    numRegistered = IntegerField(default=0, verbose_name=u'Students Registered')
#
# Statistics model - Instantiated and destroyed on use by utils_statistics.
# See utils_statistics.genCharts for corresponding chart usage
#
class PercentByTimeAllLoc(Model):
    date = CharField(max_length=30, verbose_name=u'Date')
    time = CharField(max_length=30, verbose_name=u'Time')
    percentRegistered = IntegerField(default=0, verbose_name=u'Percent Students Registered')

#
# Website settings
#
class WebsiteSettings(Model):
    session_length = IntegerField(default=40, verbose_name=u'Session Length')
    status_is_open = BooleanField(default=True, verbose_name=u'Reservation Status')
    mode_is_move_in = BooleanField(default=True, verbose_name=u'Website Mode')
    term_code = IntegerField(max_length=4, verbose_name=u'Term Code')

#
# HBS Parking User Model
#
class HBSParkingUser(AbstractBaseUser):

    username = CharField(max_length=30, unique=True, verbose_name=u'Username')
    first_name = CharField(max_length=30, blank=True, verbose_name=u'First Name')
    last_name = CharField(max_length=30, blank=True, verbose_name=u'Last Name')
    email = EmailField(blank=True, verbose_name=u'Email Address')

    USERNAME_FIELD = 'username'
    objects = UserManager()

    #
    # A set of flags for each user that decides what the user can and cannot see.
    # Flags are determined by which tools a user needs to fill his/her job description.
    #
    is_staff = BooleanField(default=False)  # access to all tools as well as staff tools
    is_developer = BooleanField(default=False)  # full access to resnet internal

    #
    # A set of flags that keeps a record of each user's reservation.
    #
    has_reserved = BooleanField(default=False)  # determines whether the user can change/view his/her reservation (one cannot change a reservation one has not made)

    class Meta:
        verbose_name = u'ResNet Internal User'
        verbose_name_plural = u'ResNet Internal Users'

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    #
    # Returns the first_name plus the last_name with a space in between and the possible '- ADMIN' removed.
    #
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, re.sub(r' - ADMIN', '', self.last_name))
        return full_name.strip()

    #
    # Returns the username with the possible '-admin' removed.
    #
    def get_alias(self):
        return re.sub(r'-admin', '', self.username)

    #
    # Sends an email to this User.
    #
    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
