from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    """модель для сотрудника"""

    name = models.CharField(max_length=200, verbose_name="ФИО", blank=True, null=True)
    first_name = None
    last_name = None
    position = models.CharField(
        max_length=200,
        verbose_name="Должность",
        blank=True,
        null=True,
        help_text="Должность",
    )

    def __str__(self):
        if self.name is not None:
            return f"{self.name}"
        return f"{self.username}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
