# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request_url', models.CharField(max_length=2083, blank=True)),
                ('request_method', models.CharField(max_length=10, blank=True)),
                ('get_data', models.TextField(blank=True)),
                ('post_data', models.TextField(blank=True)),
                ('request_body', models.TextField(blank=True)),
                ('cookies', models.TextField(blank=True)),
                ('meta', models.TextField(blank=True)),
                ('exception_type', models.CharField(max_length=255, blank=True)),
                ('exception_message', models.CharField(max_length=255, blank=True)),
                ('stack_trace', models.TextField(blank=True)),
                ('user_id', models.CharField(max_length=255, blank=True)),
                ('user_name', models.CharField(max_length=255, blank=True)),
                ('request_browser', models.CharField(max_length=255, blank=True)),
                ('request_os', models.CharField(max_length=255, blank=True)),
                ('request_device', models.CharField(max_length=255, blank=True)),
                ('is_mobile', models.BooleanField(default=False)),
                ('is_tablet', models.BooleanField(default=False)),
                ('is_touch_capable', models.BooleanField(default=False)),
                ('is_pc', models.BooleanField(default=False)),
                ('is_bot', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Error Log',
                'verbose_name_plural': 'Error Logs',
            },
        ),
    ]
