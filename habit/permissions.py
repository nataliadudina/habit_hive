from rest_framework import permissions

from habit.models import Habit


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    The user can only see and edit their own data.
    """

    def has_object_permission(self, request, view, obj):
        # Allows GET requests to any user
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Habit):
            return obj.user == request.user
        else:
            return obj == request.user
