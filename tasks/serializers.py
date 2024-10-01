from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
    task = TaskSerializer(read_only=True)
    deadline = serializers.DateTimeField(read_only=True)
    employee = serializers.CharField(read_only=True)
