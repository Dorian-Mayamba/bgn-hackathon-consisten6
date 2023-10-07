from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name="hello"),
    path('', views.index, name="index")
]

## add your views here