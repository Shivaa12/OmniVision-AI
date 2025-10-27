from rest_framework import serializers
from .models import Vehicle, VehicleLog


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "id", "registration_no", "fuel_type", "vehicle_type", "owner_name", 
            "owner_contact", "commercial_agency_name", "assigned_camera", 
            "is_authorized", "created_at", "updated_at"
        ]


class VehicleLogSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(), source="vehicle", write_only=True
    )

    class Meta:
        model = VehicleLog
        fields = ["id", "vehicle", "vehicle_id", "timestamp", "camera_id", "is_authorized"]


