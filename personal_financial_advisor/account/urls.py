from django.urls import path
from . import views


urlpatterns = [
    path('users/create', views.create_account, name="create users"),
    path('users/get', views.get_users, name="get users"),
    path('users/login', views.login, name="login users")
    # path("", views.hello, name="hello")
   
]