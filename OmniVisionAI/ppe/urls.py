from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import WorkerViewSet, PPEDetectionLogViewSet

router = DefaultRouter()
router.register(r'workers', WorkerViewSet, basename='worker')
router.register(r'logs', PPEDetectionLogViewSet, basename='ppe-log')

urlpatterns = []
urlpatterns += router.urls


