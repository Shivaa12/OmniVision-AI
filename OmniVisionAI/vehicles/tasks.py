from celery import shared_task
from .models import Vehicle, VehicleLog
from core.models import Camera, Alert
import random


@shared_task
def process_frame_for_anpr(camera_id: int):
    camera = Camera.objects.filter(id=camera_id, is_active=True).first()
    if not camera:
        return {"status": "no-camera"}
    vehicle = Vehicle.objects.order_by('?').first()
    if not vehicle:
        # create a dummy vehicle
        plate = f"TEST{random.randint(100,999)}"
        vehicle = Vehicle.objects.create(plate_number=plate, is_authorized=random.choice([True, False]))
    log = VehicleLog.objects.create(vehicle=vehicle, camera=camera, is_authorized=vehicle.is_authorized)
    if not vehicle.is_authorized:
        Alert.objects.create(module=Alert.Module.VEHICLES, severity=Alert.Severity.WARNING, message=f"Unauthorized vehicle {vehicle.plate_number}")
    return {"status": "ok", "vehicle": vehicle.plate_number, "authorized": vehicle.is_authorized}


