from django.db import models

from config import settings


class Task(models.Model):
    """модель задачи"""

    CREATED = "CREATED"
    FINISHED = "FINISHED"
    STARTED = "IN PROGRESS"

    TASK_STATUS_CHOICES = (
        (CREATED, "Создана"),
        (FINISHED, "Завершена"),
        (STARTED, "В работе"),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Автор",
        related_name="created_tasks",
        null=True,
        blank=True,
    )

    performer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Исполнитель",
        related_name="tasks",
        null=True,
        blank=True,
    )

    title = models.TextField(verbose_name="Наименование", help_text="Наименование")

    description = models.TextField(
        verbose_name="Описание",
        help_text="Описание",
        null=True,
        blank=True,
    )

    parent = models.ForeignKey(
        "Task",
        on_delete=models.SET_NULL,
        verbose_name="Родительская задача",
        related_name="children",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name="Дата/время создания", auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name="Дата/время обновления", auto_now=True
    )

    deadline = models.DateTimeField(verbose_name="Срок исполнения", null=True)

    status = models.CharField(
        choices=TASK_STATUS_CHOICES,
        max_length=200,
        default=CREATED,
        verbose_name="Статус",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["id"]
