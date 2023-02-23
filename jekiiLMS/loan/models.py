from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from member.models import Member
from user.models import Credit_Officer

#Loan Prouct model starts here

REPAYMENT_FREQUENCY_CHOICES = (
    ('onetime','ONETIME'),
    ('daily', 'DAILY'),
    ('weekly','WEEKLY'),
    ('monthly','MONTHLY'),
)

# REPAYMENT_TYPE_CHOICES = (
#     ('days','DAYS'),
#     ('weeks', 'WEEKS'),
#     ('months','MONTHS'),
# )

INTEREST_TYPE_CHOICES = (
    ('flat_rate','FLAT RATE'),
    ('reducing_balance', 'REDUCING BALANCE'),
)

SERVICE_FEE_TYPE_CHOICES = (
    ('fixed_value','FIXED VALUE'),
    ('percentage_of_principal', 'p.c of Principal'),
)

PENALTY_FEE_TYPE_CHOICES = (
    ('fixed_value','FIXED VALUE'),
    ('percentage_of_principal', 'p.c of Due Principal'),
    ('percentage_of_principal_interest', 'p.c of Due P + I'),
)

PENALTY_FREQUENCY_TYPE_CHOICES = (
    ('onetime','ONETIME'),
    ('daily', 'DAILY'),
    ('weekly', 'WEEKLY'),
    ('monthly', 'MONTHLY'),
)

INTEREST_RATE_PER_CHOICES = (
    ('day','DAY'),
    ('month','MONTH'),
    ('year','YEAR'),
)
class LoanProduct(models.Model):
    loan_product_name = models.CharField(max_length=300)
    minimum_amount = models.IntegerField(default=5000)
    maximum_amount = models.IntegerField(default=10000)
    loan_product_term = models.PositiveSmallIntegerField()
    repayment_frequency = models.CharField(max_length=8, choices=REPAYMENT_FREQUENCY_CHOICES, default='onetime')
    interest_type = models.CharField(max_length=30, choices=INTEREST_TYPE_CHOICES, default='flat_rate')
    interest_rate = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    interest_rate_per = models.CharField(max_length=50, choices=INTEREST_RATE_PER_CHOICES, default='month')
    service_fee_type = models.CharField(max_length=300, choices=SERVICE_FEE_TYPE_CHOICES, default='fixed_value')
    service_fee_value = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    penalty_type = models.CharField(max_length=300, choices=PENALTY_FEE_TYPE_CHOICES, default='fixed_value')
    penalty_value = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    penalty_frequency = models.CharField(max_length=300, choices=PENALTY_FREQUENCY_TYPE_CHOICES, default='fixed_value')
    loan_product_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.loan_product_name

#Loan Prouct model ends here

class Loan(models.Model):
    member_name = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    mobile_no = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='member_mob_no')
    id_no = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='national_id_no')
    loan_type = models.ForeignKey(LoanProduct, on_delete=models.SET_NULL, null=True)
    interest_rate = models.ForeignKey(LoanProduct, on_delete=models.SET_NULL, null=True, related_name='interest_rate_applied', default=0.3)
    payment_frequency = models.ForeignKey(LoanProduct, on_delete=models.SET_NULL, null=True, related_name='payment_frequency')
    loan_term = models.ForeignKey(LoanProduct, on_delete=models.SET_NULL, null=True, related_name='loan_term_applied', default=1)
    application_date = models.DateTimeField(auto_now_add=True)
    credit_officer = models.ForeignKey(Credit_Officer, on_delete=models.SET_NULL, null=True)
    loan_purpose = models.TextField()
    updated = models.DateTimeField(auto_now= True)
    

    class Meta:
        ordering = ['-updated', '-application_date']


    def __str__(self):
        return self.member_name

