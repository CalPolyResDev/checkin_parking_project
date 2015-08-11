# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkin_sessions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='capacity',
            field=models.PositiveSmallIntegerField(default=30, verbose_name=b'Capacity'),
            preserve_default=False,
        ),
    ]
