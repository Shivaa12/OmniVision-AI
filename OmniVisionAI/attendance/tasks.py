from celery import shared_task
from django.utils import timezone
from random import choice
from .models import Employee, AttendanceLog
from core.models import Camera, Alert


@shared_task
def process_frame_for_attendance(camera_id: int):
    camera = Camera.objects.filter(id=camera_id, is_active=True).first()
    if not camera:
        return {"status": "no-camera"}
    employee = Employee.objects.order_by('?').first()
    if not employee:
        return {"status": "no-employee"}
    AttendanceLog.objects.create(employee=employee, camera=camera)
    return {"status": "ok", "employee": employee.employee_id}


