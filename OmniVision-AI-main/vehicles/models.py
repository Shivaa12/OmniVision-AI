from django.db import models
from core.models import Camera


class Vehicle(models.Model):
    class FuelType(models.TextChoices):
        PETROL = "petrol", "Petrol"
        DIESEL = "diesel", "Diesel"
        ELECTRIC = "electric", "Electric"
        HYBRID = "hybrid", "Hybrid"
        CNG = "cng", "CNG"
        LPG = "lpg", "LPG"
    
    class VehicleType(models.TextChoices):
        PRIVATE = "private", "Private"
        COMMERCIAL = "commercial", "Commercial"
    
    registration_no = models.CharField(max_length=32, unique=True)
    fuel_type = models.CharField(max_length=32, choices=FuelType.choices, blank=True, null=True)
    vehicle_type = models.CharField(max_length=32, choices=VehicleType.choices, default=VehicleType.PRIVATE)
    owner_name = models.CharField(max_length=120, blank=True, null=True)
    owner_contact = models.CharField(max_length=20, blank=True, null=True)
    commercial_agency_name = models.CharField(max_length=120, blank=True, null=True)
    assigned_camera = models.ForeignKey('core.Camera', on_delete=models.SET_NULL, null=True, blank=True)
    is_authorized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.registration_no


class VehicleLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True)
    is_authorized = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]

from django.db import models

# Create your models here.
