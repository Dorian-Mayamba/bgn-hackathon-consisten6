from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Chat


class ChatSerializer(serializers.ModelSerializer):


    class Meta:
        model = Chat
        fields = ['message','created_at']
        