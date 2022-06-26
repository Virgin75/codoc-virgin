from django.db import models
from django.db.models import UniqueConstraint, Q
from django.conf import settings
from organizations.models import Organization

class ProjectGoal(models.Model):
    class Meta:
        verbose_name_plural = "List of goals of a project"

    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    goal = models.ForeignKey(ProjectGoal, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ProjectMember', related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProjectMember(models.Model):
    class Meta:
        unique_together = ('user', 'project',)
        verbose_name_plural = "Project members"
        # Make sure there is only 1 owner per project
        constraints = [
            UniqueConstraint(fields=['project'], condition=Q(role='OWNER'), name='unique_project_owner')
        ]

    ROLES = [
        ('OWNER', 'Owner of the project'),
        ('MEMBER', 'Member of the project'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=6, choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User: {self.user} ({self.role}) in the project: {self.project}"

class Comment(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reply_to_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content