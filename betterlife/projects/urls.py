from django.urls import path
from .views import (
    ListCreateProject,
)

urlpatterns = [
    path('projects', ListCreateProject.as_view(), name="listcreateproject"),
  
]