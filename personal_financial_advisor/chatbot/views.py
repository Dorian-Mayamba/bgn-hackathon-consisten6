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

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a financial advisor assistant that gives responses in a simple and easy-to-understand format suitable for everyone."},
            {"role": "user", "content": message},
        ])
    answer = response.choices[0].message.content.strip()
    return answer
    


# Create your views here.
@swagger_auto_schema(method='post', 
                    request_body=ChatSerializer(),
                    operation_description="This is a function to create new users.",)
@api_view(['POST'])
# def chatbot(request):
#     # chats = Chat.objects.filter(user=request.user)
    

#     if request.method == 'POST':
#         serializer = ChatSerializer(data=request.data)

#         if serializer.is_valid(): #validate the data that was passed
#             message = serializer.data['message']
#             response = ask_openai(message)


#             # chat = Chat( message=message, response=response, created_at=timezone.now())
#             # chat.save()
#             serializer.save()
#             data = {
#                 'message' : 'success',
#                 'data'  : serializer.data
#             }
#             return JsonResponse({'message':message, 'response': response})
#         else:
#             data = {
#                 'message' : 'failed',
#                 'error'  : serializer.errors
#             }
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
def chatbot(request):
    """
    View to manage chatbot interaction.

    This view accepts POST requests with a message and returns a chatbot response.
    The message and response are serialized using the ChatSerializer and saved.
    """

    if request.method == 'POST':
        serializer = ChatSerializer(data=request.data)

        if serializer.is_valid():
            message = serializer.validated_data['message']
            response = ask_openai(message)

            if response:
                # Saving the instance after making the API call and getting the response
                chat_instance = serializer.save() 
                # If you need to update the saved instance based on the response
                chat_instance.response = response 
                chat_instance.save()
                return JsonResponse({'message': message, 'response': response})
            else:
                return Response({"error": "Unable to get a response from the chatbot"}, status=500)

        return Response({"error": serializer.errors}, status=400)