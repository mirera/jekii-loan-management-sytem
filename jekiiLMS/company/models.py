from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



#credit comapny model

class Company(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10, unique=True)
    logo = models.ImageField(default='default.png', upload_to='profile_photos/')
    favicon = models.ImageField(default='default.png', upload_to='profile_photos/')
    date_joined = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100)
    site_title = models.CharField(max_length=100)

    def __str__(self):
        return self.name
