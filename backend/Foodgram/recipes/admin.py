from django.contrib import admin

from .models import Tag, Recipe, TagRecipe, IngredientRecipe


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_editable = ('color', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'name', 'text', 'pub_date', 'cooking_time'
    )
    list_editable = ('text', 'cooking_time')
    list_filter = ('name', 'author', 'tags', 'ingredients')
    search_fields = ('name', 'text', 'ingredients')


class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('tag', 'recipe')
    list_editable = ('recipe',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')
    list_editable = ('recipe',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(TagRecipe, TagRecipeAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
