# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zones', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name=b'Date')),
                ('time', models.TimeField(verbose_name=b'Time')),
                ('class_level', models.SmallIntegerField(default=3, verbose_name=b'Class Level', choices=[(0, b'Freshman'), (1, b'Transfer'), (2, b'Continuing'), (3, b'All')])),
                ('duration', models.PositiveSmallIntegerField(default=40, verbose_name=b'Duration (Minutes)')),
                ('zone', models.ForeignKey(verbose_name=b'Zone', to='zones.Zone')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
