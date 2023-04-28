from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
        validators=(validate_username,)
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        verbose_name='email',
        unique=True,
        max_length=254,
    )
    role = models.CharField(
        verbose_name='role',
        max_length=255,
        choices=ROLE_CHOICES,
        default='user',
    )
    bio = models.TextField(
        verbose_name='bio',
        blank=True
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'
