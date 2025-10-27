from rest_framework import viewsets, permissions
from users.permissions import IsAdminOrSupervisor
from .models import Worker, PPEDetectionLog
from .serializers import WorkerSerializer, PPEDetectionLogSerializer


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all().order_by("id")
    serializer_class = WorkerSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrSupervisor()]


class PPEDetectionLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PPEDetectionLog.objects.all()
    serializer_class = PPEDetectionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

from django.shortcuts import render

# Create your views here.
