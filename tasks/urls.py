from rest_framework.routers import SimpleRouter

from tasks.apps import TasksConfig
from tasks.views import TaskViewSet

app_name = TasksConfig.name

router = SimpleRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")

urlpatterns = []

urlpatterns += router.urls
