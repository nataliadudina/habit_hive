from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.paginators import HabitPaginator
from habit.permissions import IsOwnerOrReadOnly
from habit.serializers import HabitSerializer, HabitDetailSerializer


class HabitApiList(generics.ListCreateAPIView):
    """View for creating a habit or listing all user's habits."""
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Указываем текущего пользователя как автора привычки

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by('pk')


class PublicHabitApiList(generics.ListAPIView):
    """List of published habits"""
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by('pk')


class HabitDetailApiView(generics.RetrieveAPIView):
    """Shows habit details"""
    serializer_class = HabitDetailSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrReadOnly]


class HabitUpdateApiView(generics.UpdateAPIView):
    """Habit editing"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class HabitDestroyApiView(generics.DestroyAPIView):
    """Habit deletion"""
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
