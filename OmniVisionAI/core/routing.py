from django.urls import re_path
from .consumers import CameraStreamConsumer, DashboardConsumer

websocket_urlpatterns = [
    re_path(r"^ws/camera/(?P<camera_id>\d+)/$", CameraStreamConsumer.as_asgi()),
    re_path(r"^ws/dashboard/$", DashboardConsumer.as_asgi()),
]


