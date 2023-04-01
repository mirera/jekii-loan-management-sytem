from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from branch.models import Branch
from company.models import Company


#superadmin model
class SuperAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, unique=True, related_name='super_admin')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    profile_photo = models.ImageField(default='default.png', upload_to='profile_photos/')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

#loginit staff  model
class LoginitStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, unique=True, related_name='loginit_staff')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    profile_photo = models.ImageField(default='default.png', upload_to='profile_photos/')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

#credit company admin model
class CompanyAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, unique=True, related_name='company_admin')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    branch = models.OneToOneField(Branch, on_delete=models.SET_NULL, null= True)#make it default admin when processing form
    profile_photo = models.ImageField(default='default.png', upload_to='profile_photos/')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

#branch manager model
class BranchManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, unique=True, related_name='branch_manager')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    branch = models.OneToOneField(Branch, on_delete=models.SET_NULL, null= True)
    profile_photo = models.ImageField(default='default.png', upload_to='profile_photos/')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


#credit officer model
class CreditOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, unique=True, related_name='credit_officer')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    branch = models.OneToOneField(Branch, on_delete=models.SET_NULL, null= True)
    profile_photo = models.ImageField(default='default.png', upload_to='profile_photos/')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
 
