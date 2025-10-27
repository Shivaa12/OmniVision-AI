from celery import shared_task
from .models import DefectLog
from core.models import Camera, Alert
import random


@shared_task
def process_frame_for_textile(camera_id: int):
    camera = Camera.objects.filter(id=camera_id, is_active=True).first()
    if not camera:
        return {"status": "no-camera"}
    has_defect = random.random() < 0.3
    if has_defect:
        defect = random.choice(["hole", "weave-miss", "color-shift"])
        conf = round(random.uniform(0.6, 0.98), 2)
        DefectLog.objects.create(camera=camera, defect_type=defect, confidence=conf)
        if conf > 0.9:
            Alert.objects.create(module=Alert.Module.TEXTILE, severity=Alert.Severity.CRITICAL, message=f"High-confidence defect: {defect}")
        return {"status": "ok", "defect": defect, "confidence": conf}
    return {"status": "ok", "defect": None}


