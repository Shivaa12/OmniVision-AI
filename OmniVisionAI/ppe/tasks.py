from celery import shared_task
from .models import PPEDetectionLog, Worker
from core.models import Camera, Alert
import random


@shared_task
def process_frame_for_ppe(camera_id: int):
    camera = Camera.objects.filter(id=camera_id, is_active=True).first()
    if not camera:
        return {"status": "no-camera"}
    worker = Worker.objects.order_by('?').first() or Worker.objects.create(name="Worker 1")
    missing = []
    for item in ["helmet", "vest", "gloves"]:
        if random.random() < 0.2:
            missing.append(item)
    PPEDetectionLog.objects.create(worker=worker, camera=camera, missing_items=missing)
    if missing:
        Alert.objects.create(module=Alert.Module.PPE, severity=Alert.Severity.WARNING, message=f"PPE missing: {', '.join(missing)}")
    return {"status": "ok", "missing": missing}


