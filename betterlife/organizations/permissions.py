from rest_framework import permissions
from django.shortcuts import get_object_or_404
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


class CheckOrganizationObjPermission(permissions.BasePermission):
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

class CheckOrganizationMemberPermission(permissions.BasePermission):
    """
    Superusers can do any actions.
    Members of the organization can only retrieve the members of their org.
    Admin members of the organization can also add new members to their org. details.
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            if request.user.is_superuser:
                return True
            organization_id = request.GET.get('organization_id')
            organization = get_object_or_404(Organization, id=organization_id)
            membership = get_object_or_404(OrganizationMember, user=request.user, organization=organization)
            if membership:
                return True
        if request.method == 'POST':
            if request.user.is_superuser:
                return True
            organization_id = request.data['organization']
            organization = get_object_or_404(Organization, id=organization_id)
            membership = get_object_or_404(OrganizationMember, user=request.user, organization=organization)
            if membership.role == 'ADMIN':
                return True

        return False

class CheckOrganizationMemberObjPermission(permissions.BasePermission):
    """
    Superusers can do any actions.
    Admin members of the organization can update or delete members of their org. details.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'DELETE'):
            if request.user.is_superuser:
                return True
            membership = get_object_or_404(
                OrganizationMember, 
                user=request.user, 
                organization=obj.organization, 
                role='ADMIN'
            )
            print(membership)
            if membership:
                return True

        return False