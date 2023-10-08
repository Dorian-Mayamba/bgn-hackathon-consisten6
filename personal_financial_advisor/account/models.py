from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    age = models.DecimalField(decimal_places=1, max_digits=3,max_length=255,null=True)
    monthlyincome = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)

# class FinancialStatement(models.Model):
#     monthlyincome = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
#     rent_expense = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
#     food_expense = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
#     transportation_expense = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
#     utilities_expense = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)


