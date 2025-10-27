from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, AttendanceLogViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'logs', AttendanceLogViewSet, basename='attendance-log')

urlpatterns = []
urlpatterns += router.urls


