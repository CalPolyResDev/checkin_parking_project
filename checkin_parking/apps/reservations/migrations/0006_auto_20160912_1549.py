# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-12 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_auto_20160912_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationslot',
            name='last_scanned',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]