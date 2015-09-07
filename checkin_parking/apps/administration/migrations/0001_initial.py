# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import rmsconnector.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('reservation_open', models.BooleanField(verbose_name='Reservation Open', default=True)),
                ('term_code', models.PositiveSmallIntegerField(verbose_name='Term Code', default=rmsconnector.utils.get_current_term)),
                ('timeslot_length', models.PositiveSmallIntegerField(verbose_name='Time Slot Length (in Minutes)', default=40)),
            ],
            options={
                'verbose_name': 'Admin Settings',
                'verbose_name_plural': 'Admin Settings',
            },
            bases=(models.Model,),
        ),
    ]
