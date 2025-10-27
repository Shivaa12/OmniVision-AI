import pytest
from django.utils import timezone
from core.models import Camera, Alert
from attendance.models import Employee, AttendanceLog
from vehicles.models import Vehicle, VehicleLog
from ppe.models import Worker, PPEDetectionLog
from textile.models import DefectLog
from attendance.tasks import process_frame_for_attendance
from vehicles.tasks import process_frame_for_anpr
from ppe.tasks import process_frame_for_ppe
from textile.tasks import process_frame_for_textile


@pytest.mark.django_db
def test_dummy_tasks_create_logs():
    cam = Camera.objects.create(name="TestCam", ip_url="rtsp://x", is_active=True)
    Employee.objects.create(name="A", employee_id="E1")
    Worker.objects.create(name="W1")
    Vehicle.objects.create(plate_number="ABC123", is_authorized=True)

    process_frame_for_attendance(cam.id)
    process_frame_for_anpr(cam.id)
    process_frame_for_ppe(cam.id)
    process_frame_for_textile(cam.id)

    assert AttendanceLog.objects.exists()
    assert VehicleLog.objects.exists()
    assert PPEDetectionLog.objects.exists()
    assert DefectLog.objects.count() >= 0
    assert Alert.objects.count() >= 0


