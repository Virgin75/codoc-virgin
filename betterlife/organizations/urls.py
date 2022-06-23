from django.urls import path
from .views import (
    ListCreateOrganization,
    RetrieveUpdateDestroyOrganization,
)

urlpatterns = [
    path('organizations', ListCreateOrganization.as_view(), name="listcreateorg"),
    path('organizations/<int:pk>', RetrieveUpdateDestroyOrganization.as_view(), name="retrieveupdatedestroyorg"),
]