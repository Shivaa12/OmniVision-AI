from rest_framework import serializers
from .models import Worker, PPEDetectionLog


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ["id", "name", "employee_id"]


class PPEDetectionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPEDetectionLog
        fields = ["id", "worker_id", "timestamp", "missing_items", "camera_id"]


