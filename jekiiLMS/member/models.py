from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from branch.models import Branch

#the member model-- this are the borrowers
INDUSTRIES = (
    ('beauty','BEAUTY'),
    ('hospitality', 'HOSPITALITY'),
    ('retail','RETAIL'),
    ('skilled','SKILLED'),
    ('others','OTHERS'),
)

class Member(models.Model):
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    business_name = models.CharField(max_length=500, null=True)
    industry = models.CharField(max_length=500, choices=INDUSTRIES, null=True)
    address = models.CharField(max_length=500)
    date_joined = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.first_name