from django.contrib import admin

from users.models import Follow, User

from .models import (FavoriteRecipe, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag, TagRecipe)


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Управление избранными рецептами в админке."""
    list_display = ('id', 'user', 'recipe')
    list_editable = ('recipe',)


class FavoriteRecipeInline(admin.TabularInline):
    """Добавление избранных рецептов при администрировании пользователя."""
    model = FavoriteRecipe


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Управление списком покупок в админке."""
    list_display = ('id', 'user', 'recipe')
    list_editable = ('recipe',)


class ShoppingCartInline(admin.TabularInline):
    """Добавление списка покупок при администрировании пользователя."""
    model = ShoppingCart


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Управление пользователями."""
    list_display = (
        'username', 'email', 'password', 'favorite_recipes', 'shopping_recipes'
    )
    list_editable = ('email',)
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    inlines = [
        FavoriteRecipeInline, ShoppingCartInline
    ]

    def	favorite_recipes(self, row):
        """Отображение избранных рецептов."""
        return ', '.join([x.recipe.name for x in row.favorite_recipes.all()])

    def	shopping_recipes(self, row):
        """Отображение избранных рецептов."""
        return ', '.join([x.recipe.name for x in row.shopping_recipes.all()])


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Управление подписками."""
    list_display = ('id', 'user', 'following')
    list_editable = ('following',)
    search_fields = ('user', 'following')
    list_filter = ('user', 'following')
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Управление тегами в админке."""
    list_display = ('id', 'name', 'color', 'slug')
    list_editable = ('color', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Управление ингредиентами в админке."""
    list_display = ('id', 'name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    list_filter = ('name',)

class TagInline(admin.TabularInline):
    """Добавление тегов many-to-many при администрировании рецептов."""
    model = TagRecipe


class IngredientInline(admin.TabularInline):
    """Добавление ингредиентов many-to-many при администрировании рецептов."""
    model = IngredientRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Управление рецептами в админке."""
    list_display = (
        'author', 'name', 'image', 'text', 'pub_date', 'cooking_time',
        'display_tags', 'display_ingredients', 'get_favorite_count'
    )
    list_editable = ('cooking_time', 'image')
    list_filter = ('name', 'author', 'tags',)
    search_fields = ('name', 'text', 'ingredients')
    inlines = [
        IngredientInline, TagInline
    ]

    def	display_tags(self, row):
        """Отображения тегов many-to-many при администрировании рецептов."""
        return ', '.join([x.name for x in row.tags.all()])

    def	display_ingredients(self, row):
        """Отображения ingredients при администрировании рецептов."""
        return ', '.join([x.name for x in row.ingredients.all()])

    def get_favorite_count(self, obj):
        return obj.recipe_favorite.count()


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    """Управление тегами-рецептами many-to-many в админке."""
    list_display = ('tag', 'recipe')
    list_editable = ('recipe',)


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Управление ингредиентами-рецептами many-to-many в админке."""
    list_display = ('ingredient', 'recipe', 'amount')
    list_editable = ('recipe',)
