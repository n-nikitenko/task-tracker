from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee
from tasks.models import Task


class TaskTestCase(APITestCase):
    """Тестирует api задач"""

    def setUp(self):
        self.employee = Employee.objects.create(
            username="test_employee", password="testtest"
        )
        self.free_employee = Employee.objects.create(
            username="free_employee", password="testtest"
        )
        self.root_task = Task.objects.create(title="Root task", performer=self.employee)
        self.task = Task.objects.create(
            title="Test task 1", performer=self.employee, parent=self.root_task
        )
        self.task2 = Task.objects.create(
            title="Test task 2",
            performer=self.employee,
            status=Task.STARTED,
            parent=self.task,
        )

    def test_task_create(self):
        url = reverse("tasks:tasks-list")
        self.client.force_authenticate(user=self.employee)
        task_data = {"title": "Test task", "performer": self.employee.id}
        response = self.client.post(url, data=task_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("title"), task_data.get("title"))
        self.assertEqual(data.get("performer"), task_data.get("performer"))
        self.assertEqual(data.get("status"), Task.CREATED)

    def test_task_list(self):
        url = reverse("tasks:tasks-list")
        self.client.force_authenticate(user=self.employee)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data.get("results")), Task.objects.count())

    def test_task_retrieve(self):
        url = reverse("tasks:tasks-detail", args=(self.task.pk,))
        self.client.force_authenticate(user=self.employee)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.task.title)
        self.assertEqual(data.get("performer"), self.task.performer.id)

    def test_task_update(self):
        url = reverse("tasks:tasks-detail", args=(self.task.pk,))
        self.client.force_authenticate(user=self.employee)
        task_data = {"description": "test task description"}
        response = self.client.patch(url, data=task_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("description"), task_data.get("description"))

    def test_task_delete(self):
        self.client.force_authenticate(user=self.employee)
        url = reverse("tasks:tasks-detail", args=(self.task.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_important_list(self):
        self.client.force_authenticate(user=self.employee)
        url = reverse("tasks:tasks-important_tasks")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get("task").get("title"), self.task.title)
        self.assertEqual(data[0].get("employee"), self.free_employee.username)
