from django.db import models
from django.conf import settings


class Language(models.Model):
    # This model is auto populated with an update in the initial migration file
    name = models.CharField(max_length=50)
    iso_code = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name} - {self.iso_code}"


class Organization(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='OrganizationMember')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrganizationMember(models.Model):
    class Meta:
        unique_together = ('user', 'organization',)
        verbose_name_plural = "Members of organizations"

    ROLES = [
        ('ADMIN', 'Administrator of the organization'),
        ('MEMBER', 'Member of the organization'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=6, choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} in organization: {self.organization} ({self.role})"