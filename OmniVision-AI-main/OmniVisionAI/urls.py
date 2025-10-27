"""
URL configuration for OmniVisionAI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Root URL redirects to dashboard
    path('', RedirectView.as_view(url='/api/core/ui/', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('accounts/register/', auth_views.LoginView.as_view(template_name='registration/register.html'), name='register'),
    # API schema/docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/dashboard/overview/', include('core.urls')),  # includes path to overview
    # App URLs (to be implemented)
    path('api/users/', include('users.urls')),
    path('api/core/', include('core.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/vehicles/', include('vehicles.urls')),
    path('api/ppe/', include('ppe.urls')),
    path('api/textile/', include('textile.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
