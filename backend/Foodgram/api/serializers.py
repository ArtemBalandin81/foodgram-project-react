from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import (
    Tag, Ingredient, Recipe, TagRecipe, IngredientRecipe, User
)
# from recipes.validators import validate_color


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""
    # color = serializers.CharField(validators=[validate_color])
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели IngredientRecipe."""
    name = serializers.SlugField(source='ingredient.name')
    measurement_unit = serializers.SlugField(
        source='ingredient.measurement_unit'
    )
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe."""
    tags = TagSerializer(many=True, read_only=True)
    #ingredients = IngredientSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeSerializer(
        source='recipe_ingredient',
        many=True,
        read_only=True
    )
    # ИСПРАВИТЬ: пока тут "затычка"
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'text', 'cooking_time',
        )

    # ИСПРАВИТЬ: пока тут "затычка"
    def get_is_favorited(self, obj):
        return 'true'

    def get_is_in_shopping_cart(self, obj):
        return 'true'