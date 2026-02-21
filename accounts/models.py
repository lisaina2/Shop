# accounts/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # уникальное имя
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    phone = models.CharField(max_length=15, blank=True)
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # уникальное имя
        blank=True,
        help_text='User specific permissions.',
        verbose_name='user permissions',
    )

    def __str__(self):  # Добавляем этот метод
        return self.username  # Возвращаем username как строковое представление объекта
