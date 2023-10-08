from django.db import models
from account.models import User

# Create your models here.
class Chat(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE) I WIL UNCOMMENT THIS LATER WHEN I HAVE DONE THE LOGIN
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'