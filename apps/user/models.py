from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.user.choices import UserRole


class User(AbstractUser):
    role = models.CharField("Роль", choices=UserRole.choices, max_length=30)

    def __str__(self):
        return self.username
