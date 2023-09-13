from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        help_text=(_(
            'Обязательное. Например "to1@example.com".')
        ),
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
        help_text=(_(
            'Обязательное. Ваше имя.')
        ),
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False,
        help_text=(_(
            'Обязательное. Ваша фамилия.')
        ),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} follows {self.author}'
