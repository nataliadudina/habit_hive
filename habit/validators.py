from rest_framework.exceptions import ValidationError

from habit.models import Habit


class RelatedHabitAndRewardValidator:
    """Проверяет, что у новой привычки нет и связанной привычки, и вознаграждения"""

    def __init__(self, related_habit, reward):
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, data):
        related_habit = dict(data).get(self.related_habit)
        reward = dict(data).get(self.reward)

        if related_habit is not None and reward is not None:
            raise ValidationError('You have to add either a related habit or a reward')


class RelatedHabitValidator:
    """Проверяем, что связанная привычка является выработанной"""

    def __init__(self, related_habit):
        self.related_habit = related_habit

    def __call__(self, value):
        related_habit = value.get(self.related_habit)

        if related_habit is not None:
            if isinstance(related_habit, Habit):
                related_habit_id = related_habit.id
            else:
                related_habit_id = related_habit

            if related_habit_id is not None:
                try:
                    related_habit = Habit.objects.get(id=related_habit_id)
                except Habit.DoesNotExist:
                    raise ValidationError('Related habit does not exist.')

                if not related_habit.is_learned:
                    raise ValidationError(f"Habit '{related_habit.action}' is not learned yet to become a related habit.")


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
