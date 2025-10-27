"""
ASGI config for OmniVisionAI project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from core.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

django_asgi_app = get_asgi_application()

# Placeholder for websocket routes (to be populated in core.routing)
websocket_urlpatterns = websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(websocket_urlpatterns),
})

