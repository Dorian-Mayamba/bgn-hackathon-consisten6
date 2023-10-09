from django.urls import path
from . import views


urlpatterns = [
    path('users/create', views.create_account, name="create users"),
    path('users/get', views.get_users, name="get users"),
    path('user/get/<int:id>', views.get_user, name='get user'),
    path('users/login', views.login, name="login users"),
    path('users/statement/<int:user_id>', views.create_statement, name="create statement"),
    path('users/get_statement', views.get_statements, name="get statement"),
    path('users/update_statement', views.update_statements, name="update statement"),
    path('chatbot/<int:user_id>', views.Statementchatbot, name='chatbot')
    # path("", views.hello, name="hello")
   
]