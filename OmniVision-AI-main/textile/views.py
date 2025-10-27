from rest_framework import viewsets, permissions
from .models import DefectLog
from .serializers import DefectLogSerializer


class DefectLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DefectLog.objects.all()
    serializer_class = DefectLogSerializer
    permission_classes = [permissions.IsAuthenticated]

from django.shortcuts import render

# Create your views here.
