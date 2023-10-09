from django.urls import path
from . import views

urlpatterns = [
    path('message/<str:message>/<int:user_id>', views.chatbot, name='chatbot'),
]