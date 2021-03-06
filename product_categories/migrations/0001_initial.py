# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-30 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('type', models.IntegerField(choices=[(1, b'Plastic Bottle'), (2, b'Carry bags'), (3, b'Containers')])),
                ('refundable_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
    ]
