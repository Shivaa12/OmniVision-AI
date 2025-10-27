from django.db import models
from core.models import Camera


class DefectLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True)
    defect_type = models.CharField(max_length=64)
    confidence = models.FloatField(default=0.0)
    image_snapshot = models.ImageField(upload_to="textile/defects/", blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]

from django.db import models

# Create your models here.
