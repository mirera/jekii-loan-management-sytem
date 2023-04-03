from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



#credit comapny model

class Company(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Loginit Credits Ltd')
    phone_no = models.CharField(max_length=10, unique=True, default='0712345678')
    logo = models.ImageField(default='default.png', upload_to='companies_logo/')
    favicon = models.ImageField(default='default.png', upload_to='companies_logo/')
    date_joined = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    site_title = models.CharField(max_length=100, default='Lending to the unlendable')

    def __str__(self):
        return self.name
