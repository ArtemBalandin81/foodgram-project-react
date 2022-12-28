from rest_framework import serializers

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.serializers import CustomUserSerializer
from .fields import Base64ImageField


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


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

    def get_is_favorited(self, obj):
        """Метод для извлечения избранного true/false."""
        return (
            self.context['request'].user.is_authenticated
            and obj.recipe_favorite.filter(
                user=self.context['request'].user
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Метод для списка покупок true/false."""
        return (
            self.context['request'].user.is_authenticated
            and obj.recipe_shopping_list.filter(
                user=self.context['request'].user
            ).exists()
        )


class RecipeSerializerPost(RecipeSerializer):
    """Сериализатор для модели Recipe. Метод POST"""
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects)
    ingredients = IngredientRecipeSerializer(
        source='recipe_ingredient',
        many=True,
    )

    def validate_ingredients(self, value):
        """ Валидация ингредиентов:
        количество больше нуля и отсутствие дублирования. """

        set_ingredients = set()
        for ingredient in value:
            ingredient_id = ingredient['ingredient']['id']
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError(
                    f'Ингредиент с id: {ingredient_id} не найден в БД.'
                )
            if ingredient_id in set_ingredients:
                raise serializers.ValidationError(
                    f'Повторяющийся ингредиент с id: {ingredient_id}.'
                )
            set_ingredients.add(ingredient_id)
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть больше нуля. Укажите '
                    f'корректное количество ингредиента с id: {ingredient_id}.'
                )

        return value

    def add_ingredients_recipe(self, ingredients, value):
        """Метод для добавления ингредиентов в рецепт."""

        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    ingredient_id=ingredient['ingredient']['id'],
                    amount=ingredient['amount'],
                    recipe=value
                )
                for ingredient in ingredients
            ]
        )

    def create(self, validated_data):
        """Метод для создания рецепта."""
        ingredients = validated_data.pop('recipe_ingredient')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        recipe.tags.set(tags)

        self.add_ingredients_recipe(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Метод для обновления рецепта."""
        ingredients = validated_data.pop('recipe_ingredient')
        instance = super().update(instance, validated_data)
        instance.tags.set(validated_data.get('tags', instance.tags))
        instance.ingredients.clear()

        self.add_ingredients_recipe(ingredients, instance)
        return instance


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного."""

    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')
