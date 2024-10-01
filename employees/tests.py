from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee
from tasks.models import Task


class EmployeeTestCase(APITestCase):
    """Тестирует api сотрудников"""

    def setUp(self):
        self.employee = Employee.objects.create(
            username="test_employee", password="testtest"
        )

    def test_employee_create(self):
        url = reverse("employees:register")
        self.client.force_authenticate(user=self.employee)
        employee_data = {
            "username": "employee1",
            "password": "password1",
            "name": "Петров Петр Петрович",
            "position": "Продавец",
        }
        response = self.client.post(url, data=employee_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("username"), employee_data.get("username"))
        self.assertEqual(data.get("name"), employee_data.get("name"))
        self.assertEqual(data.get("position"), employee_data.get("position"))

    def test_employee_list(self):
        url = reverse("employees:employees_list")
        self.client.force_authenticate(user=self.employee)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), Employee.objects.count())

    def test_employee_retrieve(self):
        url = reverse("employees:employee_retrieve", args=(self.employee.pk,))
        self.client.force_authenticate(user=self.employee)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("username"), self.employee.username)
        self.assertEqual(data.get("name"), self.employee.name)
        self.assertEqual(data.get("position"), self.employee.position)

    def test_employee_update(self):
        url = reverse("employees:employee_update", args=(self.employee.pk,))
        self.client.force_authenticate(user=self.employee)
        employee_data = {"name": "Иванов Иван Иванович", "position": "менеджер"}
        response = self.client.patch(url, data=employee_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), employee_data.get("name"))
        self.assertEqual(data.get("position"), employee_data.get("position"))

    def test_employee_delete(self):
        self.client.force_authenticate(user=self.employee)
        url = reverse("employees:employee_destroy", args=(self.employee.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

    def test_busy_employees_list(self):
        self.client.force_authenticate(user=self.employee)
        url = reverse("employees:busy_employees_list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 0)
        # после назначения задачи
        Task.objects.create(title="Test task 1", performer=self.employee)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
