from django.urls import path
from .views import (
    ListCreateProject,
    RetrieveUpdateDestroyProject,
    ListCreateProjectMember,
    RetrieveUpdateDestroyProjectMember,
    ListCreateComment,
    RetrieveUpdateDestroyComment,
)

urlpatterns = [
    path('projects', ListCreateProject.as_view(), name="listcreateproject"),
    path('projects/<int:pk>', RetrieveUpdateDestroyProject.as_view(), name="retrieveupdatedestroyproject"),
    path('projects/<int:pk>/members', ListCreateProjectMember.as_view(), name="listcreateprojectmember"),
    path('projects-memberships/<int:pk>', RetrieveUpdateDestroyProjectMember.as_view(), name="retrieveupdatedestroyprojectmember"),
    path('projects/<int:pk>/comments', ListCreateComment.as_view(), name="listcreatecomment"),
    path('comments/<int:pk>', RetrieveUpdateDestroyComment.as_view(), name="retrieveupdatedestroycomment"),
]