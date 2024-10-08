# Generated by Django 4.2 on 2024-09-30 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.TextField(
                        help_text="Наименование", verbose_name="Наименование"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Описание",
                        null=True,
                        verbose_name="Описание",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата/время создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата/время обновления"
                    ),
                ),
                (
                    "deadline",
                    models.DateTimeField(null=True, verbose_name="Срок исполнения"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("CREATED", "Создана"),
                            ("FINISHED", "Завершена"),
                            ("IN PROGRESS", "В работе"),
                        ],
                        default="CREATED",
                        max_length=200,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_tasks",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="tasks.task",
                        verbose_name="Родительская задача",
                    ),
                ),
                (
                    "performer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Исполнитель",
                    ),
                ),
            ],
            options={
                "verbose_name": "Задача",
                "verbose_name_plural": "Задачи",
                "ordering": ["id"],
            },
        ),
    ]
