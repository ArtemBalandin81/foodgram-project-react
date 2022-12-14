from django.db import models
from django.contrib.auth.models import AbstractUser

from Foodgram.settings import NAME_MAX_LENGTH, EMAIL_MAX_LENGTH
from .validators import check_username


class User(AbstractUser):
    """Модель пользователя."""
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Админ'),
        (USER, 'Пользователь'),
    ]
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    #REQUIRED_FIELDS = ['email']
    username = models.CharField(
        validators=[check_username],
        max_length=NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True)
    last_name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True)
    role = models.CharField(
        max_length=max(len(value) for value, _ in ROLES),
        choices=ROLES,
        default=USER,
        verbose_name='Роль'
    )

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN
            or self.is_staff
        )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
