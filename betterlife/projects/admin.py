from django.contrib import admin
from .models import Project, ProjectGoal, ProjectMember

admin.site.register(Project)
admin.site.register(ProjectGoal)
admin.site.register(ProjectMember)