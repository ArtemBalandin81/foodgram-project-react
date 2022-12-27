"""Описания классов для кастомных миксинов."""

from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from recipes.models import Recipe
from .serializers import RecipeFavoriteSerializer


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
