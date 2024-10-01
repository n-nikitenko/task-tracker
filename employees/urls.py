from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from employees.apps import EmployeesConfig
from employees.views import (BusyEmployeeListApiView, EmployeeCreateApiView,
                             EmployeeDestroyApiView, EmployeeListApiView,
                             EmployeeRetrieveApiView, EmployeeUpdateApiView)

app_name = EmployeesConfig.name

urlpatterns = [
    path("register/", EmployeeCreateApiView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=[AllowAny]),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=[AllowAny]),
        name="token_refresh",
    ),
    path("", EmployeeListApiView.as_view(), name="employees_list"),
    path("busy/", BusyEmployeeListApiView.as_view(), name="busy_employees_list"),
    path("<int:pk>/", EmployeeRetrieveApiView.as_view(), name="employee_retrieve"),
    path("<int:pk>/update/", EmployeeUpdateApiView.as_view(), name="employee_update"),
    path("<int:pk>/delete/", EmployeeDestroyApiView.as_view(), name="employee_destroy"),
]
