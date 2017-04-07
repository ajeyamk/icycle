# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_level', models.IntegerField(default=4, choices=[(1, 'ERROR'), (2, 'DEBUG'), (3, 'WARN'), (4, 'INFO')])),
                ('request_url', models.CharField(max_length=2083, blank=True)),
                ('request_method', models.CharField(max_length=10, blank=True)),
                ('get_data', models.TextField(blank=True)),
                ('request_body', models.TextField(blank=True)),
                ('cookies', models.TextField(blank=True)),
                ('meta', models.TextField(blank=True)),
                ('exception_type', models.CharField(max_length=2083, blank=True)),
                ('message', models.TextField(blank=True)),
                ('stack_trace', models.TextField(blank=True)),
                ('user_id', models.IntegerField(null=True, blank=True)),
                ('user_name', models.CharField(max_length=255, blank=True)),
                ('request_browser', models.CharField(max_length=255, blank=True)),
                ('request_os', models.CharField(max_length=255, blank=True)),
                ('request_device', models.CharField(max_length=255, blank=True)),
                ('response_body', models.TextField(blank=True)),
                ('response_status', models.CharField(max_length=255, blank=True)),
                ('response_headers', models.TextField(blank=True)),
                ('response_content_type', models.CharField(max_length=255, blank=True)),
                ('is_mobile', models.BooleanField(default=False)),
                ('is_tablet', models.BooleanField(default=False)),
                ('is_touch_capable', models.BooleanField(default=False)),
                ('is_pc', models.BooleanField(default=False)),
                ('is_bot', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('method', models.CharField(max_length=10, blank=True)),
                ('url', models.CharField(max_length=2043, blank=True)),
                ('request_data', models.TextField(blank=True)),
                ('request_headers', models.TextField(blank=True)),
                ('response_text', models.TextField(blank=True)),
                ('response_status', models.IntegerField(null=True)),
                ('response_reason', models.CharField(max_length=255, blank=True)),
                ('response_time', models.IntegerField(blank=True)),
                ('user_id', models.IntegerField(null=True, blank=True)),
                ('user_name', models.CharField(max_length=255, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Request Log',
                'verbose_name_plural': 'Request Logs',
            },
        ),
    ]
