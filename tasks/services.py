from django.db.models import Count, Q

from tasks.models import Task


def get_important_tasks():
    """
    Запрашивает из БД задачи, которые не взяты в работу, но от них зависят другие задачи, взятые в работу.
    """
    queryset = (
        Task.objects.annotate(
            started_children_count=Count(
                "children__status", filter=Q(children__status=Task.STARTED)
            )
        )
        .filter(status=Task.CREATED, started_children_count__gte=1)
        .all()
    )
    return queryset
