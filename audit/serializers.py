from rest_framework import serializers
from .models import AuditEvent
from users.serializers import UserMiniSerializer


class AuditEventSerializer(serializers.ModelSerializer):
    """Output serializer for audit events"""
    user = UserMiniSerializer(read_only=True)
    
    class Meta:
        model = AuditEvent
        fields = ['id', 'action', 'user', 'created_at', 'metadata']
        read_only_fields = fields
