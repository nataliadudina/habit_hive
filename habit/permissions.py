from rest_framework import permissions

from habit.models import Habit


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользователь может видеть и редактировать только свои данные.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешает GET-запросы любому пользователю
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Habit):
            return obj.user == request.user
        else:
            return obj == request.user
