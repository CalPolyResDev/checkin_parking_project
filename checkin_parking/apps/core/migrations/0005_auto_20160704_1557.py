# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-04 15:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def delete_users(apps, schema_editor):
    apps.get_model('core', 'CheckinParkingUser').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160518_1654'),
        ('zones', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            delete_users
        ),
    ]
