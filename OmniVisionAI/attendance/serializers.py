from rest_framework import serializers
from .models import Employee, AttendanceLog


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id", "name", "employee_id", "role", "department", "address", 
            "emergency_contact_name", "emergency_contact_number", "shift_timing", 
            "joining_date", "id_proof", "assigned_camera", "photo", "liveness_verified", 
            "created_at", "updated_at"
        ]


class AttendanceLogSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source="employee", write_only=True
    )

    class Meta:
        model = AttendanceLog
        fields = ["id", "employee", "employee_id", "timestamp", "camera_id"]


