# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-04 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20160704_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkinparkinguser',
            name='out_of_state',
            field=models.NullBooleanField(),
        ),
    ]
