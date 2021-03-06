from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    CheckProjectPermission,
    CheckProjectObjPermission,
    CheckProjectMemberPermission,
    CheckProjectMemberObjPermission,
    CheckCommentPermission,
    CheckCommentObjPermission,
)
from .serializers import (
    ProjectSerializer,
    ProjectMemberSerializer,
    CommentSerializer,
)
from .models import (
    Project,
    ProjectMember,
    Comment,
)
from organizations.models import OrganizationMember
from organizations.paginations import x20ResultsPerPage

class ListCreateProject(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, CheckProjectPermission]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    pagination_class = x20ResultsPerPage

    def get_queryset(self):
        membership = get_object_or_404(
            OrganizationMember,
            user=self.request.user
        )
        queryset = Project.objects.filter(organization=membership.organization)
        return queryset
    
    '''
    Override create method to set the user who created the Project
    as a member of the Project (role = Owner).
    '''
    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = self.perform_create(serializer)
        project.members.add(
            request.user,
            through_defaults={'role': 'OWNER'}
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class RetrieveUpdateDestroyProject(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, CheckProjectObjPermission]
    serializer_class = ProjectSerializer
    lookup_field = 'pk'

class ListCreateProjectMember(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, CheckProjectMemberPermission]
    serializer_class = ProjectMemberSerializer
    queryset = ProjectMember.objects.all()
    pagination_class = x20ResultsPerPage

    def get_queryset(self):
        project_id = self.kwargs['pk']
        project = get_object_or_404(Project, id=project_id)

        return ProjectMember.objects.filter(project=project)
    
    def perform_create(self, serializer):
        organization_id = self.kwargs['pk']
        project = get_object_or_404(Project, id=organization_id)
        serializer.save(project=project)

class RetrieveUpdateDestroyProjectMember(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectMember.objects.all()
    permission_classes = [IsAuthenticated, CheckProjectMemberObjPermission]
    serializer_class = ProjectMemberSerializer
    lookup_field = 'pk'

class ListCreateComment(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, CheckCommentPermission]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = x20ResultsPerPage

    def get_queryset(self):
        project_id = self.kwargs['pk']
        project = get_object_or_404(Project, id=project_id)

        return Comment.objects.filter(project=project, reply_to_comment=None)
    
    def perform_create(self, serializer):
        organization_id = self.kwargs['pk']
        project = get_object_or_404(Project, id=organization_id)
        serializer.save(
            project=project,
            created_by=self.request.user
        )

class RetrieveUpdateDestroyComment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, CheckCommentObjPermission]
    serializer_class = CommentSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Soft-delete if the comment has at least 1 reply
        has_replies = Comment.objects.filter(reply_to_comment=instance).exists()
        if has_replies:
            instance.content = '<deleted comment>'
            instance.save()
            return Response({'status':'Comment was soft-deleted'}, status=status.HTTP_204_NO_CONTENT)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
