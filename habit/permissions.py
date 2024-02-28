from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользователь может видеть и редактировать только свой профиль.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешает GET-запросы любому пользователю
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class IsAuthenticatedAndOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        if obj.is_public:
            return True
        raise PermissionDenied("You do not have permission to access this habit.")
