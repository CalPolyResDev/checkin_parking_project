# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkin_sessions', '0003_auto_20140912_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='capacity',
            field=models.PositiveSmallIntegerField(default=30, verbose_name='Capacity'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='class_level',
            field=models.SmallIntegerField(default=3, choices=[(0, 'Freshman'), (1, 'Transfer'), (2, 'Continuing'), (3, 'All')], verbose_name='Class Level'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(verbose_name='Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='duration',
            field=models.PositiveSmallIntegerField(default=40, verbose_name='Duration (Minutes)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='time',
            field=models.TimeField(verbose_name='Time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='zone',
            field=models.ForeignKey(to='zones.Zone', verbose_name='Zone'),
            preserve_default=True,
        ),
    ]
