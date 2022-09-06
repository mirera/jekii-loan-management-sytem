from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

#the member model-- this are the borrowers
class Member(models.Model):
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=500)
    date_joined = models.DateTimeField(auto_now_add=True)
    business_type = models.TextField()

    def __str__(self):
        return self.first_name