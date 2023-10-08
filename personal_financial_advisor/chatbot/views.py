from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.http import JsonResponse
import openai
from django.contrib import auth
from rest_framework import status
from django.contrib.auth.models import User
from .models import Chat
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from .serializers import ChatSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes

openai_api_key = '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'
openai.api_key = openai_api_key

# def ask_openai(message):
#     response = openai.ChatCompletion.create(
#         model = 'gpt-3.5-turbo',
#         messages=[
#             {"role": "system", "content": "You are a financial advisor assistant that gives responses in a simple and easy-to-understand format suitable for everyone."},
#             {"role": "user", "content": message},
#         ])
#     answer = response.choices[0].message.content.strip()
#     return answer

def ask_openai(user_id, message):
    # Retrieve all past messages for this user, ordering by created_at
    user = User.objects.get(id=user_id)
    past_messages = Chat.objects.filter(user=user).order_by('created_at')
    
    # Create a message list to send to OpenAI including the new message
    messages = [{"role": "system", "content": "You are a helpful assistant"}]
    for msg in past_messages:
        messages.append({"role": "user", "content": msg.message})
        if msg.response:
            messages.append({"role": "assistant", "content": msg.response})
    messages.append({"role": "user", "content": message})
    
    # Now make the API request
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    answer = response.choices[0].message.content.strip()
    return answer


# Create your views here.
@swagger_auto_schema(method='post', 
                    request_body=ChatSerializer(),
                    operation_description="This is a function to create new users.",)
@api_view(['POST'])

        
# def chatbot(request):
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

def chatbot(request,user_id):
    """
    Manage chatbot interaction: Accept POST with message, return chatbot response.
    Messages are serialized using ChatSerializer and saved.
    """
    if request.method == 'POST':
        serializer = ChatSerializer(data=request.data)

        if serializer.is_valid():
            message = serializer.validated_data['message']
            
            # Assuming the user is logged in, otherwise retrieve a user by another method.
            # If users can be anonymous, you will need to adjust how chats are fetched in ask_openai.
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
            
            response = ask_openai(user_id, message)

            if response:
                chat_instance = serializer.save(response=response)
                return JsonResponse({'user':user,'message': message, 'response': response})
            else:
                return Response({"error": "Unable to get a response from the chatbot"}, status=500)

        return Response({"error": serializer.errors}, status=400)