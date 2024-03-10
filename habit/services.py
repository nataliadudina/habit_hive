from datetime import timedelta

from django.db.models import F, DateTimeField, Case, When
from django.utils import timezone
from .models import Habit


def get_habits_due_now(user):
    """
    Returns a queryset of Habit objects that are due to be performed now.
    """
    current_time = timezone.localtime(timezone.now())

    habit_list = Habit.objects.filter(
        user=user,
        start_from__lte=current_time.date(),
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        is_pleasant=False,
    ).annotate(
        new_date=Case(
            When(frequency=1, then=F('start_from') + timedelta(days=1)),
            When(frequency=2, then=F('start_from') + timedelta(days=2)),
            When(frequency=3, then=F('start_from') + timedelta(days=3)),
            When(frequency=4, then=F('start_from') + timedelta(days=4)),
            When(frequency=5, then=F('start_from') + timedelta(days=5)),
            When(frequency=6, then=F('start_from') + timedelta(days=6)),
            When(frequency=7, then=F('start_from') + timedelta(days=7)),
            output_field=DateTimeField()
        )
    )
    return habit_list
