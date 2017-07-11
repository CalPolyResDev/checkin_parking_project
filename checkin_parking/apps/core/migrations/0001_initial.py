# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckinParkingUser',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.EmailField(unique=True, verbose_name='Principal Name', max_length=75)),
                ('first_name', models.CharField(blank=True, verbose_name='First Name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='Last Name', max_length=30)),
                ('full_name', models.CharField(blank=True, verbose_name='Full Name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='Email Address', max_length=75)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, to='auth.Group', related_query_name='user', related_name='user_set', verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.')),
                ('user_permissions', models.ManyToManyField(blank=True, to='auth.Permission', related_query_name='user', related_name='user_set', verbose_name='user permissions', help_text='Specific permissions for this user.')),
            ],
            options={
                'verbose_name': 'Checkin Parking Reservation User',
            },
            bases=(models.Model,),
        ),
    ]
