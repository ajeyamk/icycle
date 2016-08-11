# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('errorlog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorlog',
            name='exception_message',
            field=models.CharField(max_length=2083, blank=True),
        ),
        migrations.AlterField(
            model_name='errorlog',
            name='exception_type',
            field=models.CharField(max_length=2083, blank=True),
        ),
    ]
