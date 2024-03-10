from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits', verbose_name='User')
    action = models.CharField(max_length=255, unique=True, verbose_name='Action')
    time = models.TimeField(verbose_name='Time')
    place = models.CharField(max_length=255, verbose_name='Place')
    frequency = models.PositiveSmallIntegerField(default=1, verbose_name='Frequency')  # days
    estimated_time = models.PositiveSmallIntegerField(default=120, verbose_name='Time to Perform')  # seconds
    start_from = models.DateField(auto_now_add=True, verbose_name='Start From')
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='new_habit', verbose_name='Linked Habit')
    is_pleasant = models.BooleanField(default=False, verbose_name='Is Learned')
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name='Reward')
    is_public = models.BooleanField(default=False, verbose_name='Is Public')

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Habit'
        verbose_name_plural = 'Habits'
