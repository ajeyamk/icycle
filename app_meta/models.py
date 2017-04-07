from __future__ import unicode_literals

from django.db import models


class KeyValueSetting(models.Model):
    key = models.CharField(
        max_length=255)
    value = models.TextField()
    added_on = models.DateTimeField(
        auto_now_add=True)
    updated_on = models.DateTimeField(
        auto_now=True)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'key value setting'
        verbose_name_plural = 'key value settings'
