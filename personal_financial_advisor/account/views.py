from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import auth
import email
import json
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status 
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User
from django.contrib.auth import login,logout
from .backends import AccountBackend
from chatbot.views import ask_openai

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
        
@swagger_auto_schema(
        method='post',
        request_body=LoginSerializer()
)
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['email']
        password = data['password']
        backend = AccountBackend()
        user = backend.authenticate(request, username=username,password=password)
        if user is not None:
            serialized_user = UserSerializer(user)
            return JsonResponse({
                'message' : 'login success',
                'data' : serialized_user.data
            })
        else:
            return JsonResponse({
                'message' : 'error'
            })
        

@swagger_auto_schema(method='get')
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

@swagger_auto_schema(
        method='post',
        request_body=FinancialStatementSerializer()
)
@api_view(['POST'])
def create_statement(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        # Deserialize the data and set the user
        data = request.data
        data['user'] = user.id  # Set the user ID in the request data

        serializer = FinancialStatementSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            data = {
                'message': 'success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message': 'failed',
                'error': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='get')
@api_view(['GET'])
def get_statements(request):
    if request.method == "GET":
         statements = FinancialStatement.objects.all()
         print("Statements fetched:", statements.values())
         # Serialize user data
         serializer = FinancialStatementSerializer(statements, many=True)
         # Return user data as JSON response
         print("Statements fetched:", statements) 
        #  return Response(serializer.data, status=status.HTTP_200_OK)
         return JsonResponse(serializer.data,safe=False)
        

@swagger_auto_schema(
        method='patch',
        request_body=FinancialStatementSerializer()
)
@api_view(['PATCH'])
def update_statements(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        statement = FinancialStatement.objects.get(user=user)
    except FinancialStatement.DoesNotExist:
        return Response({'message': 'Statement not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        # Deserialize the data and set the user (if needed)
        data = request.data
        data['user'] = user.id  # Set the user ID in the request data (if needed)

        serializer = FinancialStatementSerializer(statement, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = {
                'message': 'success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': 'failed',
                'error': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
@swagger_auto_schema(method='post', 
                    request_body=StatementChatSerializer(),
                    operation_description="This is a function to create new users.",)
@api_view(['POST'])
def Statementchatbot(request,user_id):
    """
    View to manage chatbot interaction.

    This view accepts POST requests with a message and returns a chatbot response.
    The message and response are serialized using the ChatSerializer and saved.
    """

    if request.method == 'POST':
        financial_statement = FinancialStatement.objects.get(user=user_id)  
        if financial_statement:
            # Manually set the message you want to send to the chatbot
            message_template = """   You are a financial advisor. What can you tell me about my financial situation below? Also, consider the following:
                    1. The currency is {currency}
                    2. The earnings for the current month are {monthlyincome}
                    #this will be the sum of the individual expenditure
                    3. My Monthly Rent/Morgage is {rent}
                    #this will be the difference between the total expenditure and monthly income
                    4. My current food expense is {food}
                    5. My current transpotation cost is {transportation}
                    6. My current utility cost is {utility}
                    7. My Miscellaneous cost are {miscellaneous}
                    8. My Dispoable income is {dispoable}
                    9. My current debt is {debt}
                    10. I want to pay my debt back in {months} months
                    11. My age is {age} years old
                    12. My financial goal is {goal}
                    13. My risk tolerance is  {tolerance}
                    Write a tailored financial plan based on the personal goals with recomendations based of the data, be specific, and include the numbers from the list above. Also
                    give tailored advice on finacial vehicles that can be used to benefit the individual 
                    and include the numbers from the list above.
                    In your response introduce theories, concepts, and explain your reasoning in a way that is simple and digestable for all age groups. In youre recomendations dont state a finacial advisor because you are the financial advisor"""
            message = message_template.format(
                monthlyincome=financial_statement.monthlyincome,
                rent=financial_statement.rent_expense,
                currency = financial_statement.currency,
                food = financial_statement.food_expense,
                transportation = financial_statement.transportation_expense,
                utility = financial_statement.utilities_expense,
                miscellaneous = financial_statement.miscellaneous_expense,
                disposable = financial_statement.disposable_income,
                debt = financial_statement.current_debt,
                months = financial_statement.time_to_pay,
                age = financial_statement.user.age,
                goal = financial_statement.current_goal,
                tolerance = financial_statement.risk_tolerance,



                
            )    
                # Call the chatbot function with the predefined message
            response = ask_openai(message)

            if response:
                # Create a serializer instance manually to save the interaction
                serializer = StatementChatSerializer(data={'message': message, 'response': response})

                if serializer.is_valid():
                    # Save the instance after making the API call and getting the response
                    chat_instance = serializer.save() 
                    return JsonResponse({'message': message, 'response': response})
                else:
                    return Response({"error": serializer.errors}, status=400)
            else:
                return Response({"error": "Unable to get a response from the chatbot"}, status=500)

        return Response({"error": "Invalid HTTP method"}, status=405)