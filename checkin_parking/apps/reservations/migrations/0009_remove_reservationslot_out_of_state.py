# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-01 16:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0008_auto_20170723_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservationslot',
            name='out_of_state',
        ),
    ]