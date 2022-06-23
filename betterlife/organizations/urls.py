from django.urls import path
from .views import (
    ListCreateOrganization,
    RetrieveUpdateDestroyOrganization,
    ListCreateOrganizationMember,
    RetrieveUpdateDestroyOrganizationMember,
)

urlpatterns = [
    path('organizations', ListCreateOrganization.as_view(), name="listcreateorg"),
    path('organizations/<int:pk>', RetrieveUpdateDestroyOrganization.as_view(), name="retrieveupdatedestroyorg"),
    path('members', ListCreateOrganizationMember.as_view(), name="listcreateorgmembers"),
    path('memberships/<int:pk>', RetrieveUpdateDestroyOrganizationMember.as_view(), name="retrieveupdatedestroyorgmember"),
]