from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tasks.models import Task
from tasks.paginators import TaskPaginator
from tasks.serializers import ImportantTaskSerializer, TaskSerializer
from tasks.services import get_important_tasks


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получение списка задач. \n"
        "ordering = created_at | performer | author | "
        "updated_at | status | parent | deadline"
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(operation_description="Создание задачи"),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Получение данных задачи по id"
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Обновление данных задачи по id"
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Удаление задачи по id"),
)
@method_decorator(
    name="important_tasks",
    decorator=swagger_auto_schema(
        operation_description="Получение списка важных задач\n"
        "ordering = created_at | performer | author | "
        "updated_at | status | parent | deadline"
    ),
)
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    pagination_class = TaskPaginator
    queryset = Task.objects.all()
    filterset_fields = ("performer__id", "parent", "performer", "author")
    search_fields = (
        "title",
        "description",
        "status",
        "performer__username",
        "performer__name",
    )
    ordering_fields = ("created_at", "performer", "author", "updated_at", "status", "parent", "deadline")

    @action(["GET"], url_path=r"important", url_name="important_tasks", detail=False)
    def important_tasks(self, request):
        """Список важных задач"""
        serializer = ImportantTaskSerializer(get_important_tasks(), many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """проверка, что в качестве родительской задачи указана другая задача"""
        parent = serializer.validated_data.get("parent")
        if parent and parent.id == self.get_object().id:
            raise ValidationError(
                "Нельзя в качестве родительской задачи указать эту же задачу"
            )
        super().perform_update(serializer)
