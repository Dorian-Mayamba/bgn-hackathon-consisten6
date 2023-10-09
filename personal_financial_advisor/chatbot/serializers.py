from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    response = serializers.CharField(read_only=True)
    class Meta:
        model = Chat
        fields = ['message','created_at', 'response']
        