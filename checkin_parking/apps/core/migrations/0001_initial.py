# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('checkin_sessions', '0004_auto_20150901_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterBuilding',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Building Name')),
            ],
            options={
                'db_table': 'building',
                'managed': False,
                'verbose_name': 'Building',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MasterCommunity',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Community Name')),
            ],
            options={
                'verbose_name_plural': 'Communities',
                'db_table': 'community',
                'managed': False,
                'verbose_name': 'Community',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CheckinParkingUser',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('username', models.CharField(max_length=30, verbose_name='Principal Name', unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Last Name')),
                ('full_name', models.CharField(blank=True, max_length=30, verbose_name='Full Name')),
                ('email', models.EmailField(blank=True, max_length=75, verbose_name='Email Address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_name='user_set', to='auth.Group', related_query_name='user', blank=True, verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.')),
                ('reservation', models.ForeignKey(default=None, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='checkin_sessions.Session', null=True)),
                ('user_permissions', models.ManyToManyField(related_name='user_set', to='auth.Permission', related_query_name='user', blank=True, verbose_name='user permissions', help_text='Specific permissions for this user.')),
            ],
            options={
                'verbose_name': 'Checkin Parking Reservation User',
            },
            bases=(models.Model,),
        ),
    ]
