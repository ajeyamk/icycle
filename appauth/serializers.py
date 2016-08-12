from __future__ import unicode_literals

from rest_framework import serializers
from .models import AppUser

DATE_FORMAT = '%d %b %Y'


class AppUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    image = serializers.ImageField(allow_null=True)
    dateOfBirth = serializers.DateTimeField(format=DATE_FORMAT, allow_null=True, source='date_of_birth')
    sex = serializers.CharField(max_length=1, allow_null=True, allow_blank=True)
    phoneNumber = serializers.CharField(max_length=20, source='phone_number')
    addressLine1 = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, source='address_line_1')
    addressLine2 = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, source='address_line_2')
    city = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    state = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    postalCode = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, source='postal_code')
    country = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = AppUser
        fields = (
            'name', 'email', 'sex', 'image', 'dateOfBirth',
            'phoneNumber', 'addressLine1', 'addressLine2', 'city', 'state',
            'postalCode', 'country', 'is_active')
