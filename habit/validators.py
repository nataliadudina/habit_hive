from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from habit.models import Habit


class RelatedHabitAndRewardValidator:
    """Проверяет, что у новой привычки нет и связанной привычки, и вознаграждения"""

    def __init__(self, related_habit, reward):
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, data):
        related_habit = data.get(self.related_habit)
        reward = data.get(self.reward)

        if related_habit and reward:
            raise ValidationError('You have to add either a related habit or a reward.')

    # def __init__(self, instance):
    #     self.instance = instance

    # def validate(self, attrs):
    #     reward = attrs.get('reward')
    #     related_habit = attrs.get('related_habit')
    #
    #     # Проверка наличие связанной привычки при создании привычки
    #     if related_habit and reward:
    #         raise ValidationError('You have to add either a related habit or a reward.')
    #
    #     # Проверка наличие связанной привычки при редактировании привычки
    #     else:
    #         if self.instance and self.instance.related_habit:
    #             related_habit = self.instance.related_habit
    #             if related_habit and reward:
    #                 raise ValidationError('You have to add either a related habit or a reward.')


class RelatedHabitValidator:
    """Проверяем, что связанная привычка является выработанной"""

    def __init__(self, related_habit):
        self.related_habit = related_habit

    def __call__(self, data):
        related_habit = data.get(self.related_habit)

        if related_habit and not related_habit.is_learned:
            raise ValidationError(
                f"Habit '{related_habit.action}' is not learned yet to become a related habit.")


class LearnedHabitValidator:
    """Проверяет, что у выработанной привычки нет связанной привычки или вознаграждения"""

    def __init__(self, related_habit, is_learned, reward):
        self.related_habit = related_habit
        self.is_learned = is_learned
        self.reward = reward

    def __call__(self, data):
        related_habit = data.get(self.related_habit)
        is_learned = data.get(self.is_learned)
        reward = data.get(self.reward)

        if is_learned:
            if related_habit or reward:
                raise ValidationError('Learned habit should have no related habits or rewards.')


class TimeSequenceValidator:
    """Проверяет, что новая привычка выполняется после выработанной привычки"""

    def __init__(self, related_habit, time):
        self.related_habit = related_habit
        self.time = time

    def __call__(self, data):
        related_habit = data.get(self.related_habit)
        habit_time = data.get(self.time)

        if related_habit:
            if related_habit.time and habit_time:
                if related_habit.time > habit_time:
                    raise ValidationError('New habit should be done after the related habit.')

    # def __init__(self, instance):
    #     self.instance = instance

    # def validate(self, attrs):
    #     habit_time = attrs.get('time')
    #     related_habit = attrs.get('related_habit')
    #
    #     # Проверка наличие связанной привычки при создании привычки
    #     if related_habit and habit_time:
    #         related_habit_instance = Habit.objects.filter(pk=related_habit.pk).first()
    #         if related_habit_instance and related_habit_instance.time > habit_time:
    #             raise ValidationError('New habit should be done after the related habit.')
    #     # Проверка наличие связанной привычки при редактировании привычки
    #     else:
    #         if self.instance and self.instance.related_habit:
    #             related_habit = self.instance.related_habit
    #             if related_habit.time and habit_time:
    #                 if related_habit.time > habit_time:
    #                     raise ValidationError('New habit should be done after the related habit.')



