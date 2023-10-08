from django.urls import path
from . import views


urlpatterns = [
    path('users/create', views.create_account, name="create users"),
    path('users/get', views.get_users, name="get users"),
    path('users/login', views.login, name="login users"),
    path('users/statement', views.create_statement, name="create statement"),
    path('users/get_statement', views.get_statements, name="get statement")
    # path("", views.hello, name="hello")
   
]