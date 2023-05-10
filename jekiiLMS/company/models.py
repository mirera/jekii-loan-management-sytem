from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User




class Package(models.Model):
    name= models.CharField(max_length=100)
    annual_price = models.CharField(max_length=100)
    monthly_price = models.CharField(max_length=100)
    employees = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    #date_added = models.DateField(auto_now_add=True)
    #modules = models.ManyToManyField(Models)

    def __str__(self):
        return self.name
    


STATUS = (
    ('active','ACTIVE'),
    ('inactive', 'INACTIVE')
)
#organization model
class Organization(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10, default='0712345678')
    logo = models.ImageField(default='default.png', upload_to='companies_logo/')
    date_joined = models.DateTimeField(auto_now_add=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=30, default='active')
    is_license_expired = models.BooleanField(default=False) 
    address = models.CharField(max_length=100, default= 'SomeStreet')
    shortcode = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.name

