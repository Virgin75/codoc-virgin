from rest_framework import permissions
from .models import Organization, OrganizationMember

class IsSuperUser(permissions.BasePermission):
    """
    User level permission to allow only superusers
    to proceed.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


class CheckOrganizationPermission(permissions.BasePermission):
    """
    Superusers can do any actions.
    Members of the organization can only retrieve the details of their org.
    Admin members of the organization can also update their org. details.
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return True if request.user.is_superuser else False
        if request.method == 'GET':
            if request.user.is_superuser:
                return True
            if obj.members.filter(id=request.user.id).exists():
                return True
        if request.method == 'PATCH':
            if request.user.is_superuser:
                return True
            if obj.members.through.objects.filter(role='ADMIN', organization=obj, user=request.user).exists():
                return True
        return False