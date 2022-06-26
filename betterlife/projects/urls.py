from django.urls import path
from .views import (
    ListCreateProject,
    RetrieveUpdateDestroyProject,
    ListCreateProjectMember,
)

urlpatterns = [
    path('projects', ListCreateProject.as_view(), name="listcreateproject"),
    path('projects/<int:pk>', RetrieveUpdateDestroyProject.as_view(), name="retrieveupdatedestroyproject"),
    path('projects/<int:pk>/members', ListCreateProjectMember.as_view(), name="listcreateprojectmember"),
]