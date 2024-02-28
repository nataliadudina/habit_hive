from django.core.validators import MaxValueValidator
from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    action = models.CharField(max_length=255, unique=True)
    time = models.TimeField()
    place = models.CharField(max_length=255)
    frequency = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(7)])  # days
    estimated_time = models.PositiveSmallIntegerField(default=120, validators=[MaxValueValidator(120)])  # seconds
    start_from = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='new_habit')
    is_learned = models.BooleanField(default=False)
    reward = models.CharField(max_length=255, null=True, blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.action
