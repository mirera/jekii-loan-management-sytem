from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal

#Branch model for a branch
ACTIVE_CHOICES = (
    ('yes','YES'),
    ('no','NO'),
)
class Branch(models.Model):
    name = models.CharField(max_length=500)
    open_date = models.DateTimeField(auto_now_add=True)
    capital = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    active = models.CharField(max_length=10, choices=ACTIVE_CHOICES)
    notes = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name