from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    age = models.DecimalField(decimal_places=1, max_digits=3,max_length=255,null=True)


class FinancialStatement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    monthlyincome = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
    rent_expense = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
    current_balance = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
    food_expense = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
    transportation_expense = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
    utilities_expense = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
    miscellaneous_expense = models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
    disposable_income =  models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
    current_debt =  models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
    time_to_pay =  models.DecimalField(decimal_places=1, max_digits=3, max_length=255,null=True)
    risk_tolerance = models.CharField(max_length=255, null=False)
    current_goal = models.CharField(max_length=255, null=False)
    currency = models.CharField(max_length=255, null=False)

class SatatementChat(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE) I WIL UNCOMMENT THIS LATER WHEN I HAVE DONE THE LOGIN
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'



