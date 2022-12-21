from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import permission_classes
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
)

from .permissions import (
    IsAuthorOrReadOnly,
)

from recipes.models import (
    Tag, Ingredient, Recipe, TagRecipe, IngredientRecipe,
)

from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeSerializerPost
)


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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipeSerializer
        return RecipeSerializerPost
