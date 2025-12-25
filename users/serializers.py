from rest_framework import serializers
from .models import User


class UserMiniSerializer(serializers.ModelSerializer):
    """Minimal user data for nested responses"""
    class Meta:
        model = User
        fields = ['id', 'name', 'email']
        read_only_fields = ['id', 'name', 'email']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']
