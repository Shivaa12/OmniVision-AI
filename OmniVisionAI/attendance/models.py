from django.db import models
from core.models import Camera


class Employee(models.Model):
    class Role(models.TextChoices):
        MANAGER = "manager", "Manager"
        SUPERVISOR = "supervisor", "Supervisor"
        OPERATOR = "operator", "Operator"
        TECHNICIAN = "technician", "Technician"
        SECURITY = "security", "Security"
        MAINTENANCE = "maintenance", "Maintenance"
    
    class Shift(models.TextChoices):
        MORNING = "morning", "Morning (6AM-2PM)"
        AFTERNOON = "afternoon", "Afternoon (2PM-10PM)"
        NIGHT = "night", "Night (10PM-6AM)"
        DAY = "day", "Day (8AM-5PM)"
    
    name = models.CharField(max_length=120)
    employee_id = models.CharField(max_length=64, unique=True)
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.OPERATOR)
    department = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=120, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)
    shift_timing = models.CharField(max_length=32, choices=Shift.choices, default=Shift.DAY)
    joining_date = models.DateField(blank=True, null=True)
    id_proof = models.FileField(upload_to="employees/id_proofs/", blank=True, null=True)
    assigned_camera = models.ForeignKey('core.Camera', on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(upload_to="employees/photos/", blank=True, null=True)
    embedding = models.BinaryField(blank=True, null=True)
    liveness_verified = models.BooleanField(default=False, help_text="Whether liveness detection was completed during registration")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.employee_id})"


class AttendanceLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]

from django.db import models

# Create your models here.
