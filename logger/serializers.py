from __future__ import unicode_literals

from rest_framework import serializers


from .models import (
    Log,
    RequestLog,
)


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


class RequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestLog
        fields = '__all__'
