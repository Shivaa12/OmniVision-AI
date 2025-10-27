from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DefectLogViewSet

router = DefaultRouter()
router.register(r'logs', DefectLogViewSet, basename='defect-log')

urlpatterns = []
urlpatterns += router.urls


