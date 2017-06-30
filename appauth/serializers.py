from rest_framework import serializers
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from appauth.constants import FailureMessages

from .models import (
    AppUser,
)


class AppUserSerializer(serializers.ModelSerializer):
    phone_regex = RegexValidator(regex=r'^\d{10}$',
                                 message="Phone number must contain only and upto 10 digits.")
    name_regex = RegexValidator(r'^[a-zA-Z\s]+$', "Only letters and spaces are allowed in 'Name' field")
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=AppUser.objects.all(), message=FailureMessages.EMAIL_ALREADY_EXISTS.value)],
        max_length=255, )
    firstName = serializers.CharField(
        validators=[name_regex],
        max_length=255,
        allow_blank=True,
        required=False,
        trim_whitespace=True,
        source='first_name')
    lastName = serializers.CharField(
        validators=[name_regex],
        max_length=255,
        allow_blank=True,
        required=False,
        trim_whitespace=True,
        source='last_name')
    phoneNumber = serializers.CharField(
        validators=[phone_regex],
        max_length=20,
        allow_blank=True,
        source='phone_number')

    class Meta:
        model = AppUser
        fields = ('phoneNumber', 'email', 'firstName', 'lastName')
