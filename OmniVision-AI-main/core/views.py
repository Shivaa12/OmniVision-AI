from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Camera, Alert, Gate, GateAccessLog, UnrecognizedFace
from .serializers import CameraSerializer, AlertSerializer, GateSerializer, GateAccessLogSerializer, UnrecognizedFaceSerializer


@login_required
def dashboard(request):
    context = {
        "now": timezone.now(),
        # Placeholder metrics; will be replaced by real aggregations
        "metrics": {
            "workers_present": 0,
            "ppe_compliance": 0,
            "vehicles_authorized": 0,
            "vehicles_unauthorized": 0,
            "defects_current": 0,
            "alerts": 0,
        }
    }
    return render(request, "core/dashboard.html", context)


@login_required
def unified_dashboard(request):
    role = getattr(request.user, "role", "operator")
    from django.middleware.csrf import get_token
    return render(request, "dashboard.html", {
        "user_role": role,
        "csrf_token": get_token(request)
    })


class IsAdminOrSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        role = getattr(request.user, "role", None)
        return role in ("admin", "supervisor")


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all().order_by("-created_at")
    serializer_class = CameraSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [IsAdminOrSupervisor()]


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def dashboard_overview(request):
    from attendance.models import AttendanceLog
    from ppe.models import PPEDetectionLog
    from vehicles.models import VehicleLog
    from textile.models import DefectLog

    workers_present = AttendanceLog.objects.filter(timestamp__date=timezone.now().date()).values("employee_id").distinct().count()
    ppe_logs = PPEDetectionLog.objects.filter(timestamp__date=timezone.now().date())
    total_ppe = ppe_logs.count() or 1
    compliant = ppe_logs.filter(missing_items=[]).count()
    ppe_compliance = int((compliant / total_ppe) * 100)
    vehicles_auth = VehicleLog.objects.filter(timestamp__date=timezone.now().date(), is_authorized=True).count()
    vehicles_unauth = VehicleLog.objects.filter(timestamp__date=timezone.now().date(), is_authorized=False).count()
    defects = DefectLog.objects.filter(timestamp__date=timezone.now().date()).count()
    
    # Gate control data
    gates = Gate.objects.filter(is_active=True)
    gates_locked = gates.filter(status=Gate.Status.LOCKED).count()
    gates_unlocked = gates.filter(status=Gate.Status.UNLOCKED).count()
    active_cameras = Camera.objects.filter(is_active=True).count()
    
    data = {
        "workers_present": workers_present,
        "ppe_compliance": ppe_compliance,
        "vehicles": {"authorized": vehicles_auth, "unauthorized": vehicles_unauth},
        "textile_defects": defects,
        "gates": {"total": gates.count(), "locked": gates_locked, "unlocked": gates_unlocked},
        "active_cameras": active_cameras,
        "alerts": AlertSerializer(Alert.objects.order_by("-timestamp")[:10], many=True).data,
    }
    return Response(data)


class GateViewSet(viewsets.ModelViewSet):
    queryset = Gate.objects.all().order_by("-created_at")
    serializer_class = GateSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class GateAccessLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GateAccessLog.objects.all().order_by("-timestamp")
    serializer_class = GateAccessLogSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["POST"])
def gate_control(request, gate_id):
    # Allow both authenticated and unauthenticated for now (development mode)
    # In production, you may want to enforce authentication
    try:
        gate = Gate.objects.get(id=gate_id)
        action = request.data.get('action')
        
        if action == 'unlock':
            gate.unlock()
            # Log the action
            GateAccessLog.objects.create(
                gate=gate,
                access_type='manual',
                user=request.user,
                details=f"Manual unlock by {request.user.username}"
            )
            display_name = gate.gate_name or gate.gate_number
            return Response({"status": "unlocked", "message": f"Gate {display_name} unlocked"})
        
        elif action == 'lock':
            gate.lock()
            # Log the action
            GateAccessLog.objects.create(
                gate=gate,
                access_type='manual',
                user=request.user,
                details=f"Manual lock by {request.user.username}"
            )
            display_name = gate.gate_name or gate.gate_number
            return Response({"status": "locked", "message": f"Gate {display_name} locked"})
        
        elif action == 'rename':
            new_name = request.data.get('new_name', '').strip()
            if not new_name:
                return Response({"error": "Gate name cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check for duplicate names
            existing_gate = Gate.objects.filter(gate_name=new_name).exclude(id=gate_id).first()
            if existing_gate:
                return Response({"error": "Gate name already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            gate.gate_name = new_name
            gate.save()
            
            # Log the action
            GateAccessLog.objects.create(
                gate=gate,
                access_type='manual',
                user=request.user,
                details=f"Gate renamed to {new_name} by {request.user.username}"
            )
            return Response({"status": "renamed", "message": f"Gate renamed to {new_name}"})
        
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Gate.DoesNotExist:
        return Response({"error": "Gate not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """Health check endpoint for system status"""
    try:
        from django.db import connection
        from django.core.cache import cache
        from celery import current_app
        
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check Redis cache
        cache.set('health_check', 'ok', 10)
        cache_result = cache.get('health_check')
        
        # Check Celery
        celery_stats = current_app.control.inspect().stats()
        
        health_status = {
            "status": "healthy",
            "database": "connected",
            "cache": "connected" if cache_result == 'ok' else "disconnected",
            "celery": "connected" if celery_stats else "disconnected",
            "timestamp": timezone.now().isoformat()
        }
        
        return Response(health_status)
    
    except Exception as e:
        return Response({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": timezone.now().isoformat()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def unrecognized_faces_count(request):
    """Get count of unrecognized faces"""
    pending_count = UnrecognizedFace.objects.filter(status='pending').count()
    return Response({"count": pending_count})


class UnrecognizedFaceViewSet(viewsets.ModelViewSet):
    queryset = UnrecognizedFace.objects.all().order_by('-detected_at')
    serializer_class = UnrecognizedFaceSerializer
    
    def get_permissions(self):
        if self.action in ["list", "retrieve", "count"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
