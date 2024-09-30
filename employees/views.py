from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from employees.models import Employee
from employees.serializers import EmployeeSerializer


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


class EmployeeUpdateApiView(UpdateAPIView):
    """обновление данных сотрудника"""

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeDestroyApiView(DestroyAPIView):
    """удаление данных сотрудника"""

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
