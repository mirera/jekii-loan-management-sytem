from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User

#Branch model for a branch
ACTIVE_CHOICES = (
    ('active','ACTIVE'),
    ('inactive','INACTIVE'),
)
class Branch(models.Model):
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=10)
    email= models.EmailField()
    open_date = models.DateTimeField(auto_now_add=False)
    capital = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    office = models.CharField(max_length=500)
    status = models.CharField(max_length=10, choices=ACTIVE_CHOICES, default='Inactive')
    notes = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name 

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name 


class Expense(models.Model):
    expense_date = models.DateField()
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    amount= models.IntegerField()
    branch= models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    note = models.TextField(null=True, blank=True)
    attachement = models.FileField(null=True, blank=True)
    
    class Meta:
        ordering = ['-expense_date']


    def __str__(self):
        return self.note[0:50] 