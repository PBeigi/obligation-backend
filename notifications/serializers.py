from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Output serializer for notifications"""
    is_read = serializers.SerializerMethodField()
    obligation = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'type', 'obligation', 'metadata', 'is_read', 'read_at', 'created_at']
        read_only_fields = fields
    
    def get_is_read(self, obj):
        """Derive is_read from read_at"""
        return obj.read_at is not None
    
    def get_obligation(self, obj):
        """Return minimal obligation data if present"""
        if obj.obligation:
            return {
                'id': obj.obligation.id,
                'title': obj.obligation.title
            }
        return None
