from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer

from .models import User
from django.core.files.base import ContentFile


class MyUserSerializer(UserSerializer):
    """Сериализатор для модели User."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )

    # ИСПРАВИТЬ: пока тут "затычка"
    def get_is_subscribed(self, obj):
        return 'false'


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для модели User."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'password'
        )

    # ИСПРАВИТЬ: пока тут "затычка"
    def get_is_subscribed(self, obj):
        return 'false'
