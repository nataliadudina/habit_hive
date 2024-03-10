from rest_framework.exceptions import ValidationError


class RelatedHabitAndRewardValidator:
    """ Checks that the new habit does not have both a related habit and a reward """

    def __init__(self, related_habit, reward):
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, data):
        related_habit = data.get(self.related_habit)
        reward = data.get(self.reward)

        if related_habit and reward:
            raise ValidationError('You may add either a related habit or a reward.')


class RelatedHabitValidator:
    """ Verify that the related habit is a learned habit """

    def __init__(self, related_habit):
        self.related_habit = related_habit

    def __call__(self, data):
        related_habit = data.get(self.related_habit)

        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                f"Habit '{related_habit.action}' is not learned yet to become a related habit.")


class LearnedHabitValidator:
    """ Checks that the learned habit does not have an related habit or reward """

    def __init__(self, related_habit, is_pleasant, reward):
        self.related_habit = related_habit
        self.is_pleasant = is_pleasant
        self.reward = reward

    def __call__(self, data):
        related_habit = data.get(self.related_habit)
        is_pleasant = data.get(self.is_pleasant)
        reward = data.get(self.reward)

        if is_pleasant:
            if related_habit or reward:
                raise ValidationError('Learned habit should have no related habits or rewards.')


class TimeSequenceValidator:
    """ Checks that the new habit is performed after the learned habit """

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
