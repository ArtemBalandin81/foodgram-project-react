from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets, mixins, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import permission_classes
#from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from rest_framework.response import Response
from django.http import JsonResponse

from .models import User, Follow

from .serializers import (
    FollowSerializer,
    FollowCreateSerializer
)


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для отражения подписок пользователя."""
    serializer_class = FollowSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)

'''
# Собираем вьюсет, который будет уметь создавать или удалять отдельный объект.
class CreateDeleteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    pass


# Создает подписку, но ответ 201 не соответствует ожиданиям
class SubscribeViewSet(CreateDeleteViewSet):
    """Вьюсет для оформления подписки пользователя."""

    serializer_class = FollowCreateSerializer
    #serializer_class = FollowSerializer

    def user_pk(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, following=self.user_pk())
'''

# Создание подписки на основании низкоуровнего класса ViewSet
class SubscribeViewSet(viewsets.ViewSet):
    """Вьюсет для создания и удаления подписки пользователя."""

    def create(self, request, user_id):
        following = get_object_or_404(User, pk=user_id)
        if following != request.user and (
            not request.user.follower.filter(following=following).exists()
        ):
            Follow.objects.create(
                user=request.user,
                following=following
            )
            serializer = FollowSerializer(
                following, context={'request': request}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)
        return JsonResponse(
            {'errors': 'Подписка уже существует, или подписка на самого себя'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, user_id):
        following = get_object_or_404(User, pk=user_id)
        data_follow = request.user.follower.filter(following=following)
        if data_follow.exists():
            data_follow.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        return JsonResponse(
            {'errors': 'Подписки для удаления не существует'},
            status=status.HTTP_400_BAD_REQUEST
        )
