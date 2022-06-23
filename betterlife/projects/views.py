from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    CheckProjectPermission,
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