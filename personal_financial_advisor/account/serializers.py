from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import *


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
        fields = ['id','first_name','last_name','email', 'password', 'age']   
class FinancialStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialStatement
        fields = ['user_id','monthlyincome','rent_expense','utilities_expense','food_expense','transportation_expense','miscellaneous_expense', 'disposable_income', 'current_debt', 'time_to_pay', 'risk_tolerance', 'current_goal', 'currency']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)   


class StatementChatSerializer(serializers.ModelSerializer):


    class Meta:
        model = SatatementChat
        fields = ['message','created_at']