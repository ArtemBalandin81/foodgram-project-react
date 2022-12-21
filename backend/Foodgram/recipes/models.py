from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from .validators import validate_color
from users.models import (User,)

# Используем свою модель пользователи из приложения users!!!
#User = get_user_model()


class Tag(models.Model):
    """Модель тега"""
    name = models.CharField(
        blank=False, max_length=200, verbose_name='Название'
    )
    color = ColorField(
        validators=[validate_color],
        max_length=7,
        verbose_name='Цвет в HEX',
        blank=False,
        default='#FFFFE0'
    )
    slug = models.SlugField(
        blank=False,
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'color', 'slug'],
                name='unique_tag'
            ),
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов"""
    name = models.CharField(
        blank=False, max_length=200, verbose_name='Ингредиенты'
    )
    measurement_unit = models.CharField(
        blank=False, max_length=200, verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_measurement_unit'
            ),
        ]

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    """Модель рецепта"""
    author = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации',
    )
    name = models.CharField(
        blank=False, max_length=200, verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=False,
        null=True,
        default=None,
        verbose_name='Фото'
    )
    text = models.TextField(blank=False, verbose_name='Текст рецепта')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        through='IngredientRecipe',
        verbose_name='Список ингредиентов',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        through='TagRecipe',
        verbose_name='Список тегов',
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:15]


class TagRecipe(models.Model):
    """Модель для связи id Tag и id Recipe."""
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tag',
    )

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngredientRecipe(models.Model):
    """Модель для связи id Ingredient, id Recipe и кол-ва ингредиентов."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient'
    )
    amount = models.FloatField(
        validators=[MinValueValidator(0)],
        verbose_name='Количество ингредиента'
    )

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'
