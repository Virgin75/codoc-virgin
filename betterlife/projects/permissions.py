from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Project, ProjectMember, Comment
from organizations.models import OrganizationMember, Organization


class CheckProjectPermission(permissions.BasePermission):
    """
    Permission used in ListCreateAPIView:
    If a user tries to create a project in an organization where he 
    does not belong, he should not have access
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
            
        if request.method == 'POST':
            if request.user.is_superuser:
                return True
            organization_id = request.data['organization']
            organization = get_object_or_404(Organization, id=organization_id)
            membership = get_object_or_404(
                OrganizationMember,
                user=request.user,
                organization=organization
            )
            if membership:
                return True
           
        return False
