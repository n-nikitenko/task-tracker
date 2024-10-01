from rest_framework import serializers

from employees.models import Employee
from tasks.serializers import TaskSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "username", "password", "email", "position", "name")
        optional_fields = ("email", "position", "name")
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }


class EmployeeUpdateSerializer(EmployeeSerializer):
    class Meta:
        model = Employee
        fields = ("id", "username", "email", "position", "name")
        optional_fields = ("email", "position", "name")
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"read_only": True},
        }


class BusyEmployeeSerializer(EmployeeSerializer):
    tasks = TaskSerializer(many=True)
    count = serializers.IntegerField()

    class Meta(EmployeeSerializer.Meta):
        fields = (
            "id",
            "username",
            "password",
            "email",
            "position",
            "name",
            "count",
            "tasks",
        )
