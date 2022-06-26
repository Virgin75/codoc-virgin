from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Project, ProjectMember, Comment
from organizations.models import OrganizationMember, Organization


class CheckProjectPermission(permissions.BasePermission):
    """
    Permission used in ListCreateAPIView:
    > If a user tries to create a project in an organization where he 
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
            membership = organization.members.filter(
                id=request.user.id,
            )
            if membership.exists():
                return True
           
        return False

class CheckProjectObjPermission(permissions.BasePermission):
    """
    Permission used in RetrieveUpdateDestroyAPIView:
    > Any members of an organization can retreve one of its projects details.
    > Only org. admin, project owner, or project member can edit a project.
    > Only org. admin or project owner can delete a project.
    """
    def has_object_permission(self, request, view, obj):
        org = obj.organization
        org_membership = org.members.through.objects.filter(
                user=request.user,
                organization=org
        )
        project_membership = obj.members.through.objects.filter(
            user=request.user,
            project=obj
        )

        if request.method == 'GET':
            if org_membership.exists() or request.user.is_superuser:
                return True
            
        if request.method == 'PATCH':
            if request.user.is_superuser:
                return True
            if org_membership.exists() and org_membership[0].role == 'ADMIN':
                return True
            if project_membership.exists():
                return True
            
        if request.method == 'DELETE':
            if request.user.is_superuser:
                return True 
            if org_membership.exists() and org_membership[0].role == 'ADMIN':
                return True
            if project_membership.exists() and project_membership[0].role == 'OWNER':
                return True
              
        return False

class CheckProjectMemberPermission(permissions.BasePermission):
    """
    Permission used in ListCreateProjectMemberAPIView:
    > The list of project members is only available to company/project members
    > Only org admins can create a new project member
    """
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['pk'])
        organization = project.organization
        org_membership = organization.members.through.objects.filter(
                user=request.user,
                organization=organization
        )
        project_membership = project.members.filter(id=request.user.id)
        print(request.user, org_membership, project_membership)

        if request.method == 'GET':
            if request.user.is_superuser:
                return True
            if org_membership.exists() or project_membership.exists():
                return True

        if request.method == 'POST':
            if request.user.is_superuser:
                return True
            if org_membership.exists() and org_membership[0].role == 'ADMIN':
                return True

        return False
