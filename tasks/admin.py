from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "performer", "status", "deadline", "parent")

    list_filter = ("status", "deadline", "performer")
    search_fields = ("title", "description")
