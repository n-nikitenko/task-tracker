from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    """модель для сотрудника"""

    name = models.CharField(max_length=200, verbose_name="ФИО", blank=True, null=True)
    position = models.CharField(
        max_length=200,
        verbose_name="Должность",
        blank=True,
        null=True,
        help_text="Должность",
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
