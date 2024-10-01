from pprint import pprint

from employees.services import get_least_busy_employee
from tasks.models import Task


def get_important_tasks():
    """
    Запрашивает из БД задачи, которые не взяты в работу, но от них зависят другие задачи, взятые в работу.

    Реализует поиск по сотрудникам, которые могут взять такие задачи (наименее загруженный сотрудник или сотрудник,
    выполняющий родительскую задачу, если ему назначено максимум на 2 задачи больше,
    чем у наименее загруженного сотрудника).

    Возвращает список объектов в формате: {Важная задача, Срок, ФИО сотрудника}.
    """
    queryset = Task.objects.exclude(parent__isnull=True).filter(
        parent__status=Task.CREATED, status=Task.STARTED
    )
    max_delta = 2
    tasks = [task.parent for task in queryset.all()]
    least_busy_employee = get_least_busy_employee()
    pprint(vars(least_busy_employee))
    result = []
    for task in tasks:
        ret_task = {
            "task": task,
            "deadline": task.deadline,
            "employee": least_busy_employee,
        }
        if task.parent is not None and task.parent.performer is not None:
            employee = task.parent.performer
            employee_active_tasks_count = employee.tasks.filter(
                status__in=[Task.CREATED, Task.STARTED]
            ).count()
            ret_task["employee"] = (
                employee
                if employee_active_tasks_count - max_delta
                <= least_busy_employee.active_tasks_count
                else least_busy_employee
            )
        result.append(ret_task)
    return result
