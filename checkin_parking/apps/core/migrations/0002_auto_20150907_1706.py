# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import checkin_parking.apps.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='checkinparkinguser',
            managers=[
                ('objects', checkin_parking.apps.core.models.CheckinParkingUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='checkinparkinguser',
            name='building',
            field=models.CharField(verbose_name='Building', blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='checkinparkinguser',
            name='email',
            field=models.EmailField(verbose_name='Email Address', blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='checkinparkinguser',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', blank=True, related_name='user_set'),
        ),
        migrations.AlterField(
            model_name='checkinparkinguser',
            name='last_login',
            field=models.DateTimeField(verbose_name='last login', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='checkinparkinguser',
            name='username',
            field=models.EmailField(verbose_name='Principal Name', max_length=254, unique=True),
        ),
    ]
