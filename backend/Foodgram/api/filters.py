import django_filters as filters

from recipes.models import Ingredient, Recipe, Tag

RECIPE_CHOICES = (
    (0, 'Not_In_List'),
    (1, 'In_List'),
)


class RecipeFilter(filters.FilterSet):
    """Фильтр рецептов по тегам, списку избранного, покупкам и автору."""
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.ChoiceFilter(
        choices=RECIPE_CHOICES,
        method='get_filtered'
    )
    is_in_shopping_cart = filters.ChoiceFilter(
        choices=RECIPE_CHOICES,
        method='get_filtered'
    )
    author = filters.NumberFilter(field_name='author__id', lookup_expr='exact')

    def get_filtered(self, queryset, name, value):
        """Фильтрация списка рецептов по избранному и списку покупок."""
        user = self.request.user
        if user.is_authenticated:
            if value == '1':
                if name == 'is_favorited':
                    queryset = queryset.filter(recipe_favorite__user=user)
                if name == 'is_in_shopping_cart':
                    queryset = queryset.filter(recipe_shopping_list__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')


class IngredientFilter(filters.FilterSet):
    """Фильтр выбора ингредиентов."""
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
