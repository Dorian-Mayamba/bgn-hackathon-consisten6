from django.db import models
from account.models import User

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats') 
    message = models.CharField(max_length=255)
    response = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}: {self.message}'