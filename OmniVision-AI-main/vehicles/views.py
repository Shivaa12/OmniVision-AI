from rest_framework import viewsets, permissions
from users.permissions import IsAdminOrSupervisor
from .models import Vehicle, VehicleLog
from .serializers import VehicleSerializer, VehicleLogSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by("registration_no")
    serializer_class = VehicleSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [IsAdminOrSupervisor()]


class VehicleLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VehicleLog.objects.select_related("vehicle").all()
    serializer_class = VehicleLogSerializer
    permission_classes = [permissions.IsAuthenticated]

from django.shortcuts import render

# Create your views here.
