from rest_framework import serializers

from .models import (
    Post,
)


class PostSerializer(serializers.ModelSerializer):
    # Exposing is_active as isActive to make JSON standards
    isActive = serializers.BooleanField(
        source='is_active')
    addedOn = serializers.DateTimeField(
        source='added_on',
        required=False,
        allow_null=True)

    class Meta:
        model = Post
        fields = (
            'title', 'category', 'body', 'isActive', 'addedOn')
