from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.paginators import HabitPaginator
from habit.permissions import IsAuthenticatedAndOwner
from habit.serializers import HabitSerializer, HabitDetailSerializer


class HabitApiList(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Указываем текущего пользователя как автора привычки

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by('pk')


class PublicHabitApiList(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by('pk')


class HabitDetailApiView(generics.RetrieveAPIView):
    serializer_class = HabitDetailSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticatedAndOwner]


class HabitUpdateApiView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticatedAndOwner]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class HabitDestroyApiView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticatedAndOwner]
