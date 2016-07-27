from django.db import models
import django
from django.contrib.auth.models import User
from django.utils import timezone
class userProfile(models.Model):
    user_ID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    joining_date = models.DateField()
    company = models.CharField(max_length=100)

    def __str__(self):
        return self.user_ID.username

    def email(self):
        return self.user_ID.email

    def full_name(self):
        return self.user_ID.first_name + " " + self.user_ID.last_name

class Expenses(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.CharField(max_length=100,default="Groceries")

    spent_amount = models.IntegerField(default=0)
    spent_date = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=300,default = "self Explainable!!")

    def __str__(self):
        return self.user_name.username

    def email(self):
        return self.user_id.email

    def full_name(self):
        return self.user_name.first_name + " " + self.user_name.last_name

