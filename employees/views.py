from django.db.models import Count, Q
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from employees.models import Employee
from employees.serializers import (BusyEmployeeSerializer, EmployeeSerializer,
                                   EmployeeUpdateSerializer)
from tasks.models import Task


class EmployeeCreateApiView(CreateAPIView):
    """создание сотрудника"""

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        employee = serializer.save(is_active=True)
        employee.set_password(employee.password)
        employee.save()


class EmployeeRetrieveApiView(RetrieveAPIView):
    """получение данных сотрудника по id"""

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeListApiView(ListAPIView):
    """получение списка сотрудников"""

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filterset_fields = ("username",)
    search_fields = ("username", "name")
    ordering_fields = ("username", "name")


class EmployeeUpdateApiView(UpdateAPIView):
    """обновление данных сотрудника"""

    serializer_class = EmployeeUpdateSerializer
    queryset = Employee.objects.all()


class EmployeeDestroyApiView(DestroyAPIView):
    """удаление данных сотрудника"""

    queryset = Employee.objects.all()


class BusyEmployeeListApiView(ListAPIView):
    """получение списка занятых сотрудников и их задач, отсортированного по количеству активных задач"""

    serializer_class = BusyEmployeeSerializer

    def get_queryset(self):
        queryset = (
            Employee.objects.filter(tasks__isnull=False)
            .annotate(
                count=Count("tasks__status", filter=Q(tasks__status=Task.STARTED))
            )
            .order_by("-count")
        )
        return queryset
