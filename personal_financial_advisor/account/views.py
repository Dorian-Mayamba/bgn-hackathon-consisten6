from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import auth
import email
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status 
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from django.forms import model_to_dict
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User

# Create your views here.


@swagger_auto_schema(method='post', 
                    request_body=UserSerializer(),
                    operation_description="This is a function to create new users.",
                    responses= {201: openapi.Response("""An example success response is:
                    ``{
                        "message": "successful",
                        "data": [
                            {
                                "id": 1,
                                "first_name": "Test",
                                "last_name": "User",
                                "email": "test@user.com",
                                "phone": "234123456789",
                                "date_joined":"2022-01-26T10:33:45.239782Z"
                            }
                        ]
                    }``"""),
                        400: openapi.Response("""An example failure is:
                        ``{
                        "message": "failed",
                        "error": {
                            "email": [
                            "This field is required."
                            ],
                            "password": [
                            "This field is required."
                            ],
                            "phone": [
                            "This field is required."
                            ]
                        }``""")
                    }
)
@api_view(['POST'])
def create_account(request):
    
    if request.method == "POST":
        #Allows user to signup or create account
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data) #deserialize the data
        
        if serializer.is_valid(): #validate the data that was passed
            print("Serializer is valid. Data:", serializer.validated_data)
            serializer.save()
            data = {
                'message' : 'success',
                'data'  : serializer.data
            }
            return JsonResponse(serializer.data, status=201)
        else:
            print(serializer.data)
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_users(request):
    if request.method == "GET":
         users = User.objects.all()
         print("Users fetched:", users.values())
         # Serialize user data
         serializer = UserSerializer(users, many=True)
         # Return user data as JSON response
         print("Users fetched:", users) 
        #  return Response(serializer.data, status=status.HTTP_200_OK)
         return JsonResponse(serializer.data,safe=False)

# @swagger_auto_schema(method='post', 
#                     request_body=LoginSerializer(),
#                     operation_description="This is a function to login.",)
# @api_view(['POST'])

        
# def login(request):
#     """
#     View to manage chatbot interaction.

#     This view accepts POST requests with a message and returns a chatbot response.
#     The message and response are serialized using the ChatSerializer and saved.
#     """

#     if request.method == 'POST':
#         serializer = ChatSerializer(data=request.data)

#         if serializer.is_valid():
#             message = serializer.validated_data['message']
#             response = ask_openai(message)

#             if response:
#                 # Saving the instance after making the API call and getting the response
#                 chat_instance = serializer.save() 
#                 # If you need to update the saved instance based on the response
#                 chat_instance.response = response 
#                 chat_instance.save()
#                 return JsonResponse({'message': message, 'response': response})
#             else:
#                 return Response({"error": "Unable to get a response from the chatbot"}, status=500)

#         return Response({"error": serializer.errors}, status=400)