# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkin_sessions', '0002_session_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='capacity',
            field=models.PositiveSmallIntegerField(default=30, verbose_name=b'Capacity'),
        ),
    ]
