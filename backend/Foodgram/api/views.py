from django.db.models import Sum
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from recipes.models import (FavoriteRecipe, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag, TagRecipe)
from services.create_pdf import create_pdf
from .filters import RecipeFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeFavoriteSerializer,
                          RecipeSerializer, RecipeSerializerPost,
                          TagSerializer)


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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


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

    @action(
        methods=['GET', ],
        url_path='download_shopping_cart',
        detail=False,
    )
    def download_shopping_cart(self, request):
        """Метод для загрузки списка покупок в формате PDF."""

        user = request.user
        ingredient_list_user = (
            IngredientRecipe.objects.
            prefetch_related('ingredient', 'recipe').
            filter(recipe__recipe_shopping_list__user=user).
            values('ingredient__id').
            order_by('ingredient__id')
        )

        shopping_list = (
            ingredient_list_user.annotate(total=Sum('amount')).
            values_list(
                'ingredient__name', 'ingredient__measurement_unit', 'total'
            )
        )

        file = create_pdf(shopping_list, 'Список покупок')

        return FileResponse(
            file,
            as_attachment=True,
            filename='shopping_list.pdf',
            status=status.HTTP_200_OK
        )


class CustomCreateAndDeleteMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Кастомный миксин (создание, удаление) для
    избранных рецептов и списка покупок."""

    def custom_create(self, request, recipe_id, link_name, model):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        queryset = getattr(recipe, link_name)
        if not queryset.filter(user=request.user).exists():
            model.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = RecipeFavoriteSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(
            {'errors': f'Рецепт уже добавлен в {link_name}'},
            status.HTTP_400_BAD_REQUEST
        )

    def custom_destroy(self, request, recipe_id, link_name):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        queryset = getattr(recipe, link_name)
        data = queryset.filter(user=request.user)
        if data.exists():
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': f'Рецепта для удаления из {link_name} не существует'},
            status.HTTP_400_BAD_REQUEST
        )


class FavoriteViewSet(viewsets.ViewSet, CustomCreateAndDeleteMixin):
    """Вьюсет для создания и удаления избранного рецепта."""

    def create(self, request, recipe_id):
        link_name = 'recipe_favorite'
        model = FavoriteRecipe
        return self.custom_create(request, recipe_id, link_name, model)

    def destroy(self, request, recipe_id):
        link_name = 'recipe_favorite'
        return self.custom_destroy(request, recipe_id, link_name)


class ShoppingViewSet(viewsets.ViewSet, CustomCreateAndDeleteMixin):
    """Вьюсет для добавления и удаления рецепта в/из списка покупок."""

    def create(self, request, recipe_id):
        link_name = 'recipe_shopping_list'
        model = ShoppingCart
        return self.custom_create(request, recipe_id, link_name, model)

    def destroy(self, request, recipe_id):
        link_name = 'recipe_shopping_list'
        return self.custom_destroy(request, recipe_id, link_name)
