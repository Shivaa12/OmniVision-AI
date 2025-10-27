from django.contrib import admin
from .models import Camera, Alert, Gate, GateAccessLog


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
	list_display = ("name", "ip_url", "location", "camera_type", "purpose", "is_active", "created_at")
	list_filter = ("is_active", "camera_type", "purpose", "location")
	search_fields = ("name", "ip_url", "location")


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
	list_display = ("timestamp", "module", "severity", "message", "resolved")
	list_filter = ("module", "severity", "resolved")
	search_fields = ("message",)


@admin.register(Gate)
class GateAdmin(admin.ModelAdmin):
	list_display = ("gate_number", "camera", "status", "location", "is_active", "last_access_time")
	list_filter = ("status", "is_active", "created_at")
	search_fields = ("gate_number", "location")


@admin.register(GateAccessLog)
class GateAccessLogAdmin(admin.ModelAdmin):
	list_display = ("gate", "access_type", "user", "vehicle", "employee", "timestamp")
	list_filter = ("access_type", "timestamp", "gate")
	search_fields = ("gate__gate_number", "user__username", "vehicle__registration_no", "employee__name")
