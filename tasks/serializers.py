from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from employees.services import get_least_busy_employee
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):

    def validate_deadline(self, value):
        if value < timezone.now():
            raise ValidationError("Срок выполнения задачи не может быть в прошлом")
        return value

    class Meta:
        model = Task
        fields = "__all__"
        optional_fields = ("performer", "description", "parent", "deadline", "status")
        extra_kwargs = {
            "id": {"read_only": True},
            "author": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class ImportantTaskSerializer(serializers.Serializer):
    task = SerializerMethodField()
    deadline = serializers.DateTimeField(read_only=True)
    employee = SerializerMethodField()

    @staticmethod
    def get_employee(task):
        """ возвращает наименее загруженного сотрудника или сотрудника,
        выполняющего родительскую задачу, если ему назначено максимум на 2 задачи больше,
        чем у наименее загруженного сотрудника """

        max_delta = 2
        least_busy_employee = get_least_busy_employee()
        if task.parent is not None and task.parent.performer is not None:
            employee = task.parent.performer
            employee_active_tasks_count = employee.tasks.filter(status__in=[Task.CREATED, Task.STARTED]).count()
            if employee_active_tasks_count - max_delta <= least_busy_employee.active_tasks_count:
                return str(employee)
        return str(least_busy_employee)

    @staticmethod
    def get_task(task):
        return TaskSerializer(task).data
