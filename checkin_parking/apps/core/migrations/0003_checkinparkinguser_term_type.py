# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150907_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkinparkinguser',
            name='term_type',
            field=models.CharField(max_length=15, verbose_name='Class Level', blank=True),
        ),
    ]
