from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
      Custom User model that extends Django's built-in AbstractUser model.
      """
    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(max_length=50, blank=True, null=True, default='ghost', verbose_name="Username")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='Country')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
