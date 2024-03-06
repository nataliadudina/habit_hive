from django.db.models import ExpressionWrapper, IntegerField, F
from django.utils import timezone
from .models import Habit


def get_habits_due_now(user):
    """
    Returns a queryset of Habit objects that are due to be performed now.
    """
    now = timezone.now()

    habit_list = Habit.objects.filter(
        user=user,
        start_from__lte=now.date(),
        frequency__gt=0,
        time__hour=now.hour,
        time__minute=now.minute,
    ).annotate(
        days_diff=ExpressionWrapper(
            (now.date() - F('start_from')) % F('frequency'),
            output_field=IntegerField()
        )
    ).filter(days_diff=0)

    return habit_list
