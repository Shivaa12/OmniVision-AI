from django.core.management.base import BaseCommand
from django.utils import timezone
import random

from core.models import Camera, Alert
from attendance.models import Employee, AttendanceLog
from vehicles.models import Vehicle, VehicleLog
from ppe.models import Worker, PPEDetectionLog
from textile.models import DefectLog


class Command(BaseCommand):
    help = "Seed dummy data for cameras, employees/workers, vehicles, and logs"

    def handle(self, *args, **options):
        # Cameras
        cams = []
        for idx in range(1, 3):
            cam, _ = Camera.objects.get_or_create(
                name=f"Camera {idx}",
                defaults={
                    "ip_url": f"rtsp://example.com/stream/{idx}",
                    "location": f"Zone {idx}",
                    "is_active": True,
                },
            )
            cams.append(cam)

        # Employees and Workers
        employees = []
        for idx in range(1, 6):
            emp, _ = Employee.objects.get_or_create(
                employee_id=f"E{1000+idx}",
                defaults={"name": f"Employee {idx}"},
            )
            employees.append(emp)

        workers = []
        for idx in range(1, 4):
            w, _ = Worker.objects.get_or_create(name=f"Worker {idx}")
            workers.append(w)

        # Vehicles
        vehicles = []
        for idx in range(1, 6):
            v, _ = Vehicle.objects.get_or_create(
                plate_number=f"TEST{100+idx}",
                defaults={"owner_name": f"Owner {idx}", "is_authorized": random.choice([True, False])},
            )
            vehicles.append(v)

        # Logs
        if cams:
            cam = cams[0]
            for emp in employees:
                AttendanceLog.objects.get_or_create(employee=emp, camera=cam)
            for _ in range(5):
                v = random.choice(vehicles)
                VehicleLog.objects.create(vehicle=v, camera=cam, is_authorized=v.is_authorized)
            for w in workers:
                missing = []
                for item in ["helmet", "vest", "gloves"]:
                    if random.random() < 0.3:
                        missing.append(item)
                PPEDetectionLog.objects.create(worker=w, camera=cam, missing_items=missing)
            for _ in range(5):
                if random.random() < 0.5:
                    DefectLog.objects.create(camera=cam, defect_type=random.choice(["hole", "weave-miss", "color-shift"]), confidence=round(random.uniform(0.6, 0.99), 2))

        # Sample alerts
        Alert.objects.get_or_create(module=Alert.Module.VEHICLES, message="Unauthorized vehicle TEST999", severity=Alert.Severity.WARNING)
        Alert.objects.get_or_create(module=Alert.Module.PPE, message="PPE missing: helmet", severity=Alert.Severity.WARNING)
        Alert.objects.get_or_create(module=Alert.Module.TEXTILE, message="High-confidence defect: hole", severity=Alert.Severity.CRITICAL)

        self.stdout.write(self.style.SUCCESS("Dummy data seeded."))


