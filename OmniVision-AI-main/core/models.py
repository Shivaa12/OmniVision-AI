from django.db import models
from django.utils import timezone


class Camera(models.Model):
    class Purpose(models.TextChoices):
        ATTENDANCE = "attendance", "Attendance"
        ANPR = "anpr", "ANPR (Vehicle)"
        PPE = "ppe", "PPE Monitoring"
        TEXTILE = "textile", "Textile Quality"
        GENERAL = "general", "General Monitoring"
    
    class CameraType(models.TextChoices):
        RTSP = "rtsp", "RTSP"
        HTTP = "http", "HTTP"
        USB = "usb", "USB"
        IP = "ip", "IP Camera"
    
    name = models.CharField(max_length=100)
    camera_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    location = models.CharField(max_length=120, blank=True)
    gate_name = models.CharField(max_length=100, blank=True, help_text="Associated gate name")
    ip_url = models.CharField(max_length=255, help_text="RTSP/HTTP URL for the camera stream")
    camera_type = models.CharField(max_length=32, choices=CameraType.choices, default=CameraType.IP)
    purpose = models.CharField(max_length=32, choices=Purpose.choices, default=Purpose.GENERAL)
    assigned_module = models.CharField(max_length=32, blank=True, help_text="Assigned module for this camera")
    camera_notes = models.TextField(blank=True, help_text="Additional notes or description")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} @ {self.location}" if self.location else self.name


class Gate(models.Model):
    class Status(models.TextChoices):
        LOCKED = "locked", "Locked"
        UNLOCKED = "unlocked", "Unlocked"
        MAINTENANCE = "maintenance", "Maintenance"
    
    gate_number = models.CharField(max_length=50, unique=True)
    gate_name = models.CharField(max_length=100, blank=True, help_text="Display name for the gate")
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.LOCKED)
    location = models.CharField(max_length=120, blank=True)
    last_access_time = models.DateTimeField(null=True, blank=True)
    auto_lock_duration = models.IntegerField(default=10, help_text="Auto-lock after X seconds")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        display_name = self.gate_name or f"Gate {self.gate_number}"
        return f"{display_name} ({self.status})"

    def unlock(self):
        self.status = self.Status.UNLOCKED
        self.last_access_time = timezone.now()
        self.save()

    def lock(self):
        self.status = self.Status.LOCKED
        self.save()


class Alert(models.Model):
    class Module(models.TextChoices):
        ATTENDANCE = "attendance", "Attendance"
        VEHICLES = "vehicles", "Vehicles"
        PPE = "ppe", "PPE"
        TEXTILE = "textile", "Textile"
        CORE = "core", "Core"
        GATE = "gate", "Gate Control"

    class Severity(models.TextChoices):
        INFO = "info", "Info"
        WARNING = "warning", "Warning"
        CRITICAL = "critical", "Critical"

    module = models.CharField(max_length=32, choices=Module.choices)
    message = models.TextField()
    severity = models.CharField(max_length=16, choices=Severity.choices, default=Severity.INFO)
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"[{self.severity}] {self.module}: {self.message[:50]}"


class GateAccessLog(models.Model):
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=20, choices=[
        ('manual', 'Manual Override'),
        ('auto_unlock', 'Auto Unlock'),
        ('auto_lock', 'Auto Lock'),
        ('unauthorized', 'Unauthorized Access'),
    ])
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey('attendance.Employee', on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.gate.gate_number} - {self.access_type} at {self.timestamp}"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UnrecognizedFace(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending Review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
    
    face_image = models.ImageField(upload_to='unrecognized_faces/', blank=True, null=True)
    detected_at = models.DateTimeField(auto_now_add=True)
    camera = models.ForeignKey('Camera', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_faces')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_faces')
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-detected_at']
        verbose_name_plural = "Unrecognized Faces"
    
    def __str__(self):
        return f"Unrecognized Face at {self.detected_at} ({self.status})"
