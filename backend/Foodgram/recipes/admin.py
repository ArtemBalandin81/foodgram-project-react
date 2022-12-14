from django.contrib import admin

from .models import Tag, Recipe, TagRecipe, IngredientRecipe, Ingredient
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password')
    list_editable = ('email',)
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Управление тегами в админке"""
    list_display = ('name', 'color', 'slug')
    list_editable = ('color', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Управление ингредиентами в админке"""
    list_display = ('name', 'measurement_unit')
    list_editable = ('measurement_unit',)


class TagInline(admin.TabularInline):
    """Добавление тегов many-to-many при администрировании рецептов"""
    model = TagRecipe


class IngredientInline(admin.TabularInline):
    """Добавление ингредиентов many-to-many при администрировании рецептов"""
    model = IngredientRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Управление рецептами в админке"""
    list_display = (
        'author', 'name', 'image', 'text', 'pub_date',
        'cooking_time', 'display_tags', 'display_ingredients'
    )
    list_editable = ('cooking_time', 'image')
    list_filter = ('name', 'author', 'tags', 'ingredients')
    search_fields = ('name', 'text', 'ingredients')
    inlines = [
        IngredientInline, TagInline
    ]

    def	display_tags(self, row):
        """Отображения тегов many-to-many при администрировании рецептов"""
        return ', '.join([x.name for x in row.tags.all()])

    def	display_ingredients(self, row):
        """Отображения ingredients при администрировании рецептов"""
        return ', '.join([x.name for x in row.ingredients.all()])


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    """Управление тегами-рецептами many-to-many в админке"""
    list_display = ('tag', 'recipe')
    list_editable = ('recipe',)


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Управление ингредиентами-рецептами many-to-many в админке"""
    list_display = ('ingredient', 'recipe', 'amount')
    list_editable = ('recipe',)
