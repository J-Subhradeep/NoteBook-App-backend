from rest_framework import serializers
from .models import User, Note


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff',
                  'is_validated', 'is_active', 'is_superuser', 'created_at']
