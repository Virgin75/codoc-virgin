from rest_framework import serializers
from .models import (
    Project,
    ProjectMember,
    Comment,
)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = '__all__'
        read_only_fields = ['project', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['project', 'created_by', 'created_at', 'updated_at']

    def get_answers(self, obj):
        comments = Comment.objects.filter(reply_to_comment=obj.id)
        comments_serialized = CommentSerializer(comments, many=True)
        return comments_serialized.data