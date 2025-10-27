from rest_framework import serializers
from .models import DefectLog


class DefectLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectLog
        fields = ["id", "timestamp", "camera_id", "defect_type", "confidence", "image_snapshot"]


