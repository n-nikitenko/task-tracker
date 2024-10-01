from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tasks.models import Task
from tasks.paginators import TaskPaginator
from tasks.serializers import ImportantTaskSerializer, TaskSerializer
from tasks.services import get_important_tasks


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_description="Получение списка задач"),
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
    decorator=swagger_auto_schema(operation_description="Список важных задач"),
)
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    pagination_class = TaskPaginator
    queryset = Task.objects.all()

    @action(["GET"], url_path=r"important", url_name="important_tasks", detail=False)
    def important_tasks(self, request):
        """Список важных задач"""

        serializer = ImportantTaskSerializer(get_important_tasks(), many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = Task.objects.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
