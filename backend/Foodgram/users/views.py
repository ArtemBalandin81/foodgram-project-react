from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowSerializer


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для отражения подписок пользователя."""
    serializer_class = FollowSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


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
        return Response(
            {'errors': 'Подписка уже существует, или подписка на самого себя'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, user_id):
        following = get_object_or_404(User, pk=user_id)
        data_follow = request.user.follower.filter(following=following)
        if data_follow.exists():
            data_follow.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Подписки для удаления не существует'},
            status=status.HTTP_400_BAD_REQUEST
        )
