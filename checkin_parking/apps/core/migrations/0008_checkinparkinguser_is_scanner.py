# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-12 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_checkinparkinguser_out_of_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkinparkinguser',
            name='is_scanner',
            field=models.BooleanField(default=False),
        ),
    ]
