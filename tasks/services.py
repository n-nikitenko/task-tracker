from django.db.models import Count, Q

from tasks.models import Task


def get_important_tasks():
    """
    Запрашивает из БД задачи, которые не взяты в работу, но от них зависят другие задачи, взятые в работу.

    Реализует поиск по сотрудникам, которые могут взять такие задачи (наименее загруженный сотрудник или сотрудник,
    выполняющий родительскую задачу, если ему назначено максимум на 2 задачи больше,
    чем у наименее загруженного сотрудника).

    Возвращает список объектов в формате: {Важная задача, Срок, ФИО сотрудника}.
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
