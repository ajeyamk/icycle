# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255, blank=True)),
                ('sex', models.CharField(max_length=1, blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('phone_number', models.CharField(max_length=20, blank=True)),
                ('address_line_1', models.CharField(max_length=255, blank=True)),
                ('address_line_2', models.CharField(max_length=255, blank=True)),
                ('city', models.CharField(max_length=255, blank=True)),
                ('state', models.CharField(max_length=255, blank=True)),
                ('postal_code', models.CharField(max_length=255, blank=True)),
                ('country', models.CharField(max_length=255, blank=True)),
                ('image', models.ImageField(upload_to='users/profile_pictures', blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('reset_password_token', models.CharField(max_length=8, blank=True)),
                ('last_updated_by', models.ForeignKey(related_name='updated_by_user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'User',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role_name', models.CharField(unique=True, max_length=255)),
                ('display_name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='appuser',
            name='roles',
            field=models.ManyToManyField(related_name='role_appuser', to='appauth.Role', blank=True),
        ),
    ]
