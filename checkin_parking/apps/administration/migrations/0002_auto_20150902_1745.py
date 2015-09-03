# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import rmsconnector.utils


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminsettings',
            name='term_code',
            field=models.PositiveSmallIntegerField(default=rmsconnector.utils.get_current_term, verbose_name='Term Code'),
        ),
    ]
