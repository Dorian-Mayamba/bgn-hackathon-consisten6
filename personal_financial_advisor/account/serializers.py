from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import User 


class UserSerializer(serializers.ModelSerializer):

    # password = serializers.CharField(write_only=True)

    # def create(self, validated_data):

    #     user = myuser.objects.create_user(
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #         age=validated_data['age'],
    #         monthlyincome=validated_data['monthlyincome'],
    #         name=validated_data['name'],

    #     )


    #     user.save()
    #     return user

        # return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ['name','email', 'password', 'age','monthlyincome']
        