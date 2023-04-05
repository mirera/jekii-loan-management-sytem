from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

#organization model
class Organization(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10, default='0712345678')
    logo = models.ImageField(default='default.png', upload_to='companies_logo/')
    date_joined = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100, default= 'SomeStreet 123')

    def __str__(self):
        return self.name