from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from branch.models import Branch


#all users by default are credit officer
class Credit_Officer(models.Model):
    username = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, unique=True)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    branch = models.OneToOneField(Branch, on_delete=models.SET_NULL, null= True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
 



