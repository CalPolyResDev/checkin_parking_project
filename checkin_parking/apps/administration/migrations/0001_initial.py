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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('reservation_open', models.BooleanField(verbose_name='Reservation Open', default=True)),
                ('term_code', models.IntegerField(max_length=4, verbose_name='Term Code', default=rmsconnector.utils.get_current_term)),
            ],
            options={
                'verbose_name_plural': 'AdminSettings',
            },
            bases=(models.Model,),
        ),
    ]
