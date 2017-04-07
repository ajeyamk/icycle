# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Title of the post. Max 255 chars.', max_length=255)),
                ('category', models.IntegerField(blank=True, help_text='Selectable category for the post.', null=True, choices=[(1, 'Science'), (2, 'Artificial Intelligence / Machine Learning'), (3, 'Nature'), (4, 'Philosophy')])),
                ('body', models.TextField(help_text='The actual body of the post.', blank=True)),
                ('is_active', models.BooleanField(help_text='If the post is active or not.')),
                ('added_on', models.DateTimeField(help_text='Creation timestamp.', auto_now_add=True)),
                ('updated_on', models.DateTimeField(help_text='Last updation timestamp.', auto_now=True)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
    ]
