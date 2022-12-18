from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import permission_classes
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
)

from recipes.models import (
    Tag, Ingredient, Recipe, TagRecipe, IngredientRecipe,
)

from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
)


@permission_classes([AllowAny])
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет (контроллер) для модели Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    # permission_classes = (IsAdminOrReadOnly,)
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ('slug',)


@permission_classes([AllowAny])
class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет (контроллер) для модели Tag."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    # permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)

@permission_classes([IsAuthenticatedOrReadOnly])
class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет (контроллер) для модели Recipe."""
    #queryset = Recipe.objects.all().annotate(amount='ingredients__amount')
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
