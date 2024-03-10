from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.paginators import HabitPaginator
from habit.permissions import IsOwnerOrReadOnly
from habit.serializers import HabitSerializer, HabitDetailSerializer


class HabitApiList(generics.ListCreateAPIView):
    """ View for creating a habit or listing all user's habits """
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Указываем текущего пользователя как автора привычки

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by('pk')


class PublicHabitApiList(generics.ListAPIView):
    """ List of published habits """
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by('pk')


class HabitDetailApiView(generics.RetrieveAPIView):
    """ Shows habit details """
    serializer_class = HabitDetailSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrReadOnly]


class HabitUpdateApiView(generics.UpdateAPIView):
    """ Habit editing """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.instance
        related_habit = instance.related_habit
        reward = instance.reward
        time = instance.time

        if related_habit and 'reward' in serializer.validated_data:
            raise ValidationError('You may add either a related habit or a reward.')
        elif reward and 'related_habit' in serializer.validated_data:
            raise ValidationError('You may add either a related habit or a reward.')

        if instance.is_learned:
            if 'reward' in serializer.validated_data or 'related_habit' in serializer.validated_data:
                raise ValidationError('Learned habit should have no related habits or rewards.')

        if related_habit:
            related_habit_time = related_habit.time
            if time < related_habit_time:
                raise ValidationError('New habit should be done after the related habit.')

        serializer.validated_data['user'] = self.request.user
        serializer.save()


class HabitDestroyApiView(generics.DestroyAPIView):
    """ Habit deletion """
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
