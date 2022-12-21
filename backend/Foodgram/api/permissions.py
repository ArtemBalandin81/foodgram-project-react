from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """ Доступ к объекту разрешен только автору."""
    message = 'Доступ к объекту разрешен только автору.'

    def has_permissions(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if (
                request.method in SAFE_METHODS
                or obj.author == request.user
        ):
            return True
