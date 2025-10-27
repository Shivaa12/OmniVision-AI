from rest_framework import permissions


class IsAdminOrSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "is_superuser", False):
            return True
        role = getattr(user, "role", None)
        return role in ("admin", "supervisor")


