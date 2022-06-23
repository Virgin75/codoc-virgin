from rest_framework import serializers
from .models import (
    Organization,
    OrganizationMember,
)

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class OrganizationMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMember
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
