from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, VehicleLogViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'logs', VehicleLogViewSet, basename='vehicle-log')

urlpatterns = []
urlpatterns += router.urls


