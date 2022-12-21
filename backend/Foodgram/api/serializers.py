from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
#from djoser.serializers import UserSerializer, UserCreateSerializer
from users.serializers import CustomUserSerializer

from recipes.models import (
    Tag, Ingredient, Recipe, TagRecipe, IngredientRecipe
)
from users.models import User
import base64
from django.core.files.base import ContentFile
# from recipes.validators import validate_color


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Если полученный объект строка, и она начинается с 'data:image'...
        if isinstance(data, str) and data.startswith('data:image'):
            # ...начинаем декодировать изображение из base64.
            # Сначала нужно разделить строку на части.
            format, imgstr = data.split(';base64,')
            # И извлечь расширение файла.
            ext = format.split('/')[-1]
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""
    # color = serializers.CharField(validators=[validate_color])
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


# из модели IngredientRecipe оставили лишь amount и переопределили остальное
class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели IngredientRecipe."""
    name = serializers.SlugField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.SlugField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""
    #name = serializers.StringRelatedField(many=True, read_only=True)
    #measurement_unit = serializers.StringRelatedField(
    #    many=True, read_only=True
    #)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe. Метод GET"""
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    ingredients = IngredientRecipeSerializer(
        source='recipe_ingredient',
        many=True,
        read_only=True
    )
    image = Base64ImageField(required=True)
    # ИСПРАВИТЬ: пока тут "затычка"
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

    # ИСПРАВИТЬ: пока тут "затычка"
    def get_is_favorited(self, obj):
        """Метод для избранного."""
        return 'true'

    def get_is_in_shopping_cart(self, obj):
        """Метод для списка покупок."""
        return 'true'


class RecipeSerializerPost(serializers.ModelSerializer):
    """Сериализатор для модели Recipe. Метод POST"""
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects)
    ingredients = IngredientRecipeSerializer(
        source='recipe_ingredient',
        many=True,
        # read_only=True
    )
    image = Base64ImageField(use_url=False, required=True)
    cooking_time = serializers.IntegerField(
        validators=[MinValueValidator(1)]
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

    # ИСПРАВИТЬ: пока тут "затычка"
    def get_is_favorited(self, obj):
        """Метод для избранного."""
        return 'true'

    def get_is_in_shopping_cart(self, obj):
        """Метод для списка покупок."""
        return 'true'


    def create(self, validated_data):
        """Метод для создания рецепта."""
        ingredients = validated_data.pop('recipe_ingredient')
        tags = validated_data.pop('tags')

        recipe = super().create(validated_data)
        recipe.tags.set(tags)

        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    ingredient_id=ingredient['ingredient']['id'],
                    amount=ingredient['amount'],
                    recipe=recipe
                )
                for ingredient in ingredients
            ]
        )

        return recipe

    def update(self, instance, validated_data):
        """Метод для обновления рецепта."""
        ingredients = validated_data.pop('recipe_ingredient')
        #tags = validated_data.pop('tags')
        #super().update(self, instance, validated_data)

        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = (
            validated_data.get('cooking_time', instance.cooking_time)
        )
        instance.tags.set(validated_data.get('tags', instance.tags))
        instance.ingredients.clear()
        instance.save()

        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    ingredient_id=ingredient['ingredient']['id'],
                    amount=ingredient['amount'],
                    recipe=instance
                )
                for ingredient in ingredients
            ]
        )

        instance.save()
        return instance
