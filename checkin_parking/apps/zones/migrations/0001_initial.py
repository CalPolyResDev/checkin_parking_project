# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Building Name', max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Community Name', max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', max_length=30, unique=True)),
                ('capacity', models.PositiveSmallIntegerField(verbose_name='Capacity', default=30)),
                ('buildings', models.ManyToManyField(verbose_name='Building(s)', to='zones.Building')),
                ('community', models.ForeignKey(verbose_name='Community', to='zones.Community')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='building',
            name='community',
            field=models.ForeignKey(related_name='buildings', verbose_name='Community', to='zones.Community'),
            preserve_default=True,
        ),
    ]
