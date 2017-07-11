# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_auto_20150907_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationslot',
            name='class_level',
            field=models.CharField(max_length=30, default=6, choices=[('Freshman', 'Freshman'), ('Transfer', 'Transfer'), ('Continuing', 'Continuing'), ('Freshman/Transfer', 'Freshman/Transfer'), ('Freshman/Continuing', 'Freshman/Continuing'), ('Transfer/Continuing', 'Transfer/Continuing'), ('Freshman/Transfer/Continuing', 'Freshman/Transfer/Continuing')], verbose_name='Class Level'),
        ),
    ]
