from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    OrganizationSerializer,
    OrganizationMemberSerializer,
)
from .models import (
    Organization,
    OrganizationMember,
)
from .permissions import (
    IsSuperUser,
    CheckOrganizationPermission,
)
from .paginations import x20ResultsPerPage

class ListCreateOrganization(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    pagination_class = x20ResultsPerPage

    '''
    Override create method to set the user who created the Organization
    as the admin of the Organization.
    '''
    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        org = self.perform_create(serializer)
        org.members.add(
            request.user,
            through_defaults={'role': 'ADMIN'}
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class RetrieveUpdateDestroyOrganization(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    permission_classes = [IsAuthenticated, CheckOrganizationPermission]
    serializer_class = OrganizationSerializer
    lookup_field = 'pk'


# ListOrganisationMember (Admin or member) --> Superusers OR or all org members (for LIST: with ?role=admin OR member)
# CreateOrganisationMember (Admin or member) --> Superusers OR org admin
# RetrieveOrganizationMember --> superusers OR all org members
# UpdateOrganizationMember --> superusers OR org admin
# DestroyOrganizationMember --> superusers OR org admin