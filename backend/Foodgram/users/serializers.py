from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recipe

from .models import Follow, User


class CustomUserSerializer(UserSerializer):
    """Сериализатор для модели User."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        if str(request_user) == 'AnonymousUser':
            return 'false'
        return obj.following.filter(user=request_user).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для модели User."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'password'
        )

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        return obj.following.filter(user=request_user).exists()


class FollowRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe в подписках."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(CustomUserSerializer):
    """Сериализатор метода GET подписок пользователя."""
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return FollowRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()



# Эксперементальный класс создания подписки на основании модели Follow
# 201 - response не соответствует требованиям ТЗ
class FollowCreateSerializer(serializers.ModelSerializer):
    """Сериализатор методов PUT, Delete подписок пользователя."""

    class Meta:
        model = Follow
        fields = ('user', 'following')
        read_only_fields = ('user', 'following')
'''       
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]
'''
'''
    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError('Подписка на себя запрещена!')
        return value
'''