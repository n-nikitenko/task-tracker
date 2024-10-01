from django.db.models import Count, F, Min, Q, Sum
from django.db.models.functions import Coalesce

from employees.models import Employee


def get_least_busy_employee():
    """выбирает сотрудника с наименьшим количеством назначенных задач"""

    return (
        Employee.objects.annotate(
            active_tasks_count=Count(
                "tasks__status", filter=Q(tasks__status__in=["CREATED", "IN PROGRESS"])
            )
        )
        .order_by("active_tasks_count")
        .first()
    )
