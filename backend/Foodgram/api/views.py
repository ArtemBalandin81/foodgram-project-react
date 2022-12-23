from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RecipeFilter
from rest_framework import filters, permissions, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import permission_classes
from django.http import HttpResponse
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
)

from .permissions import (
    IsAuthorOrReadOnly,
)

from recipes.models import (Tag,
                            Ingredient,
                            Recipe,
                            TagRecipe,
                            IngredientRecipe,
                            FavoriteRecipe,
                            ShoppingCart)

from .serializers import (TagSerializer,
                          IngredientSerializer,
                          RecipeSerializer,
                          RecipeSerializerPost,
                          RecipeFavoriteSerializer)


@permission_classes([AllowAny])
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет (контроллер) для модели Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


@permission_classes([AllowAny])
class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет (контроллер) для модели Tag."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    # permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


#@permission_classes([IsAuthenticatedOrReadOnly])
class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет (контроллер) для модели Recipe."""
    queryset = Recipe.objects.all()
    permission_classes = [
        IsAuthorOrReadOnly,
    ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipeSerializer
        return RecipeSerializerPost


class FavoriteViewSet(viewsets.ViewSet):
    """Вьюсет для создания и удаления избранного рецепта."""

    def create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if not request.user.favorite_recipes.filter(recipe=recipe).exists():
            FavoriteRecipe.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = RecipeFavoriteSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(
            {'errors': 'Рецепт уже добавлен в избранное'},
            status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        data_favorite = request.user.favorite_recipes.filter(recipe=recipe)
        if data_favorite.exists():
            data_favorite.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепта для удаления не существует'},
            status.HTTP_400_BAD_REQUEST
        )


class ShoppingViewSet(viewsets.ViewSet):
    """Вьюсет для добавления и удаления рецепта в/из списка покупок."""

    def create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if not request.user.shopping_recipes.filter(recipe=recipe).exists():
            ShoppingCart.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = RecipeFavoriteSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(
            {'errors': 'Рецепт уже добавлен в список на покупки'},
            status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        data_favorite = request.user.shopping_recipes.filter(recipe=recipe)
        if data_favorite.exists():
            data_favorite.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепта для удаления не существует'},
            status.HTTP_400_BAD_REQUEST
        )
