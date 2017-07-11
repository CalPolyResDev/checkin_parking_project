# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('zones', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('class_level', models.PositiveSmallIntegerField(verbose_name='Class Level', default=3, choices=[(0, 'Freshman'), (1, 'Transfer'), (2, 'Continuing'), (3, 'All')])),
                ('resident', models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True, related_name='reservationslot', blank=True, verbose_name='Resident', on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Date')),
                ('time', models.TimeField(verbose_name='Time')),
                ('term', models.PositiveSmallIntegerField(verbose_name='Term Code')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reservationslot',
            name='timeslot',
            field=models.ForeignKey(related_name='reservationslots', verbose_name='Time Slot', to='reservations.TimeSlot'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reservationslot',
            name='zone',
            field=models.ForeignKey(related_name='reservationslots', verbose_name='Zone', to='zones.Zone'),
            preserve_default=True,
        ),
    ]
