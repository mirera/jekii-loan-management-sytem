from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from branch.models import Branch
from company.models import Organization


#superadmin model
class SuperAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, unique=True, related_name='super_admin')
    email = models.EmailField(default="test@test.com")
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    profile_photo = models.ImageField(default='default.png', upload_to='profile_photos/')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

#loginit staff  model
class LoginitStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, unique=True, related_name='loginit_staff')
    email = models.EmailField(default="test@test.com")
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
    email = models.EmailField(default="test@test.com")
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    company = models.OneToOneField(Organization, on_delete=models.CASCADE)
    branch = models.OneToOneField(Branch, on_delete=models.SET_NULL, null= True)#make it default admin when processing form
    profile_photo = models.ImageField(default='default.png', upload_to='profile_photos/')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

#branch manager model
class BranchManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, unique=True, related_name='branch_manager')
    email = models.EmailField(default="test@test.com")
    is_employee = models.BooleanField(default=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    company = models.OneToOneField(Organization, on_delete=models.CASCADE)
    branch = models.OneToOneField(Branch, on_delete=models.SET_NULL, null= True)
    profile_photo = models.ImageField(default='default.png', upload_to='profile_photos/')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


#credit officer model
class CreditOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, unique=True, related_name='credit_officer')
    email = models.EmailField(default="test@test.com")
    is_employee = models.BooleanField(default=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    company = models.OneToOneField(Organization, on_delete=models.CASCADE)
    branch = models.OneToOneField(Branch, on_delete=models.SET_NULL, null= True)
    profile_photo = models.ImageField(default='default.png', upload_to='profile_photos/')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

#-- role models start
class Role(models.Model): 
    company = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.name

#-- staff model
USER_TYPE = (
    ('admin','ADMIN'),
    ('staff', 'STAFF')
)

STATUS = (
    ('active','ACTIVE'),
    ('inactive','INACTIVE'),
)

class CompanyStaff(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id_no = models.CharField(max_length=10, blank=True)
    phone_no = models.CharField(max_length=10, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null= True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE)
    staff_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    profile_photo = models.ImageField(default='default.png', upload_to='profile_photos/')
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='active')

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.first_name + ' ' + self.last_name
 
