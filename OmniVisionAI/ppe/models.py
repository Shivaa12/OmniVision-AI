from django.db import models
from core.models import Camera
from attendance.models import Employee


class Worker(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.name


class PPEDetectionLog(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    missing_items = models.JSONField(default=list)
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]

from django.db import models

# Create your models here.
