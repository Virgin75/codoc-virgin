from django.shortcuts import render, get_object_or_404
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
    CheckOrganizationObjPermission,
    CheckOrganizationMemberPermission,
    CheckOrganizationMemberObjPermission,
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
        organization = self.perform_create(serializer)
        organization.members.add(
            request.user,
            through_defaults={'role': 'ADMIN'}
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class RetrieveUpdateDestroyOrganization(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    permission_classes = [IsAuthenticated, CheckOrganizationObjPermission]
    serializer_class = OrganizationSerializer
    lookup_field = 'pk'

class ListCreateOrganizationMember(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, CheckOrganizationMemberPermission]
    serializer_class = OrganizationMemberSerializer
    queryset = OrganizationMember.objects.all()
    pagination_class = x20ResultsPerPage

    def get_queryset(self):
        organization_id = self.request.GET.get('organization_id')
        organization = get_object_or_404(Organization, id=organization_id)

        return OrganizationMember.objects.filter(organization=organization)

class RetrieveUpdateDestroyOrganizationMember(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrganizationMember.objects.all()
    permission_classes = [IsAuthenticated, CheckOrganizationMemberObjPermission]
    serializer_class = OrganizationMemberSerializer
    lookup_field = 'pk'