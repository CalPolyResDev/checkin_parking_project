# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-11 14:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_checkinparkinguser_is_scanner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkinparkinguser',
            name='out_of_state',
        ),
    ]
