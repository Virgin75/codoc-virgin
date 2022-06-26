from django.urls import path
from .views import (
    ListCreateProject,
    RetrieveUpdateDestroyProject,
)

urlpatterns = [
    path('projects', ListCreateProject.as_view(), name="listcreateproject"),
    path('projects/<int:pk>', RetrieveUpdateDestroyProject.as_view(), name="retrieveupdatedestroyproject"),
]