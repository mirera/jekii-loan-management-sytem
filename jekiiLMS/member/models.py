from tkinter import CASCADE
import os
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from branch.models import Branch
from company.models import Organization

#the member model-- this are the borrowers
INDUSTRIES = (
    ('beauty','BEAUTY'),
    ('hospitality', 'HOSPITALITY'),
    ('retail','RETAIL'),
    ('skilled','SKILLED'),
    ('others','OTHERS'),
)
STATUS = (
    ('active','ACTIVE'),
    ('inactive', 'INACTIVE')
)

class Member(models.Model): 
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_no = models.CharField(max_length=10, unique=True)
    phone_no = models.CharField(max_length=10, unique=True)
    email=models.EmailField(null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    business_name = models.CharField(max_length=500, null=True)
    industry = models.CharField(max_length=500, choices=INDUSTRIES, null=True)
    address = models.CharField(max_length=500)
    previous_credit_score = models.IntegerField(default=0)
    credit_score = models.IntegerField(default=0)
    date_joined = models.DateField()
    passport_photo = models.ImageField( default='default.png', upload_to='member_passports/')
    status = models.CharField(max_length=50, choices=STATUS, default='inactive', )

    #check is member has active loan
    def has_active_loan(self):
        active_loans = self.loans_as_member.filter(status__in=['pending', 'approved', 'overdue'])
        return bool(active_loans)


    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.first_name + ' ' + self.last_name