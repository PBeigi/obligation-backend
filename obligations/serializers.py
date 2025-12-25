from rest_framework import serializers
from django.utils import timezone
from .models import Obligation
from users.models import User
from users.serializers import UserMiniSerializer


class ObligationCreateSerializer(serializers.ModelSerializer):
    """Input serializer for creating obligations"""
    owed_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        help_text='User who owes the obligation'
    )
    
    class Meta:
        model = Obligation
        fields = ['title', 'description', 'owed_by', 'due_at']
    
    def validate_owed_by(self, value):
        """Prevent self-obligations"""
        request = self.context.get('request')
        if request and request.user == value:
            raise serializers.ValidationError(
                "You cannot create an obligation for yourself to owe."
            )
        return value
    
    def validate_due_at(self, value):
        """Ensure due_at is not in the past"""
        if value < timezone.now():
            raise serializers.ValidationError(
                "Due date cannot be in the past."
            )
        return value


class ObligationSerializer(serializers.ModelSerializer):
    """Output serializer for reading obligations"""
    owed_by = UserMiniSerializer(read_only=True)
    owed_to = UserMiniSerializer(read_only=True)
    
    class Meta:
        model = Obligation
        fields = [
            'id', 'title', 'description', 'status', 'due_at',
            'owed_by', 'owed_to',
            'created_at', 'updated_at', 'completed_at', 'cancelled_at'
        ]
        read_only_fields = fields
