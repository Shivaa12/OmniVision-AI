from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cameras', views.CameraViewSet, basename='camera')
router.register(r'gates', views.GateViewSet, basename='gate')
router.register(r'gate-logs', views.GateAccessLogViewSet, basename='gate-log')
router.register(r'unrecognized-faces', views.UnrecognizedFaceViewSet, basename='unrecognized-face')

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ui/', views.unified_dashboard, name='unified-dashboard'),
    path('ui/overview/', views.unified_dashboard, name='unified-dashboard-overview'),
    path('ui/attendance/', views.unified_dashboard, name='unified-dashboard-attendance'),
    path('ui/vehicles/', views.unified_dashboard, name='unified-dashboard-vehicles'),
    path('ui/ppe/', views.unified_dashboard, name='unified-dashboard-ppe'),
    path('ui/textile/', views.unified_dashboard, name='unified-dashboard-textile'),
    path('ui/cameras/', views.unified_dashboard, name='unified-dashboard-cameras'),
    path('ui/settings/', views.unified_dashboard, name='unified-dashboard-settings'),
    path('dashboard/overview/', views.dashboard_overview, name='dashboard-overview'),
    path('gates/<int:gate_id>/control/', views.gate_control, name='gate-control'),
    path('health/', views.health_check, name='health-check'),
    path('unrecognized-faces/count/', views.unrecognized_faces_count, name='unrecognized-faces-count'),
]

urlpatterns += router.urls

