from rest_framework import serializers

from .models import (
    AppUser,
)


class AppUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = '__all__'
