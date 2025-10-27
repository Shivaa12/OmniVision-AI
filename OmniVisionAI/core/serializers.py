from rest_framework import serializers
from .models import Camera, Alert, Gate, GateAccessLog, UnrecognizedFace


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ["id", "name", "camera_id", "ip_url", "location", "gate_name", "camera_type", "purpose", "assigned_module", "camera_notes", "is_active", "created_at"]


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ["id", "module", "message", "severity", "timestamp", "resolved"]


class GateSerializer(serializers.ModelSerializer):
    camera_name = serializers.CharField(source='camera.name', read_only=True)
    
    class Meta:
        model = Gate
        fields = [
            "id", "gate_number", "gate_name", "camera", "camera_name", "status", "location", 
            "last_access_time", "auto_lock_duration", "is_active", "created_at", "updated_at"
        ]


class GateAccessLogSerializer(serializers.ModelSerializer):
    gate_number = serializers.CharField(source='gate.gate_number', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    vehicle_reg = serializers.CharField(source='vehicle.registration_no', read_only=True)
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    
    class Meta:
        model = GateAccessLog
        fields = [
            "id", "gate", "gate_number", "access_type", "user", "user_name",
            "vehicle", "vehicle_reg", "employee", "employee_name", "timestamp", "details"
        ]


class UnrecognizedFaceSerializer(serializers.ModelSerializer):
    camera_name = serializers.CharField(source='camera.name', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.username', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    
    class Meta:
        model = UnrecognizedFace
        fields = [
            "id", "face_image", "detected_at", "camera", "camera_name", "location",
            "status", "reviewed_by", "reviewed_by_name", "reviewed_at",
            "assigned_to", "assigned_to_name", "notes"
        ]


