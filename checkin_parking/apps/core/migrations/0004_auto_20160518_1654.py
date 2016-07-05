# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_checkinparkinguser_term_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkinparkinguser',
            name='building',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Building'),
        ),
        migrations.AlterField(
            model_name='checkinparkinguser',
            name='term_type',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Class Level'),
        ),
    ]