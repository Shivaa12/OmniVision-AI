from rest_framework import viewsets, permissions
from users.permissions import IsAdminOrSupervisor
from .models import Employee, AttendanceLog
from .serializers import EmployeeSerializer, AttendanceLogSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by("id")
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [IsAdminOrSupervisor()]


class AttendanceLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AttendanceLog.objects.select_related("employee").all()
    serializer_class = AttendanceLogSerializer
    permission_classes = [permissions.IsAuthenticated]

from django.shortcuts import render

# Create your views here.
