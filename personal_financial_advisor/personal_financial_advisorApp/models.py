from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    saving_amount = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
