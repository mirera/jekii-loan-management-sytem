from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
import uuid
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



ACTIVE_CHOICES = (
    ('active','ACTIVE'),
    ('inactive','INACTIVE'),
)

TERM_PERIOD = (
    ('day','DAY'),
    ('week','WEEK'),
    ('month','MONTH'),
    ('year','YEAR'),
)

class LoanProduct(models.Model):
    loan_product_name = models.CharField(max_length=300)
    minimum_amount = models.IntegerField(default=5000)
    maximum_amount = models.IntegerField(default=10000)
    loan_product_term = models.PositiveSmallIntegerField()
    loan_term_period= models.CharField(max_length=20, choices=TERM_PERIOD, default='month')
    repayment_frequency = models.CharField(max_length=8, choices=REPAYMENT_FREQUENCY_CHOICES, default='onetime')
    interest_type = models.CharField(max_length=30, choices=INTEREST_TYPE_CHOICES, default='flat_rate')
    interest_rate = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    service_fee_type = models.CharField(max_length=300, choices=SERVICE_FEE_TYPE_CHOICES, default='fixed_value')
    service_fee_value = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    penalty_type = models.CharField(max_length=300, choices=PENALTY_FEE_TYPE_CHOICES, default='fixed_value')
    penalty_value = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    penalty_frequency = models.CharField(max_length=300, choices=PENALTY_FREQUENCY_TYPE_CHOICES, default='fixed_value')
    status = models.CharField(max_length=10, choices=ACTIVE_CHOICES, default='inactive')
    loan_product_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.loan_product_name

#Loan Prouct model ends here

class Loan(models.Model):
    #id_no = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='national_id_no')
    id_no = models.CharField(max_length=10)
    loan_id =models.CharField(max_length=500, null=True, unique=True)
    member_name = models.CharField(max_length=500)
    mobile_no = models.CharField(max_length=500)
    loan_type = models.CharField(max_length=500)
    interest_rate = models.IntegerField()
    payment_frequency = models.CharField(max_length=50)
    loan_term = models.PositiveSmallIntegerField()
    application_date = models.DateTimeField(auto_now_add=True)
    credit_officer = models.ForeignKey(Credit_Officer, on_delete=models.SET_NULL, null=True)
    loan_purpose = models.TextField()
    updated = models.DateTimeField(auto_now= True)


# Generate loan ID based on member ID and current timestamp
    def save(self, *args, **kwargs):
        if not self.loan_id:
            # Generate loan ID based on member ID and current timestamp
            member_id = self.id_no.id
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S%f')
            self.loan_id = f'{member_id}-{timestamp}'
        super().save(*args, **kwargs)
    
# a method that retrieves the Member object based on the provided id_no and updates the corresponding fields in the Loan object
    def update_from_member(self):
        member = Member.objects.filter(id_no=self.id_no).first()
        if member:
            self.member_name = member
            self.mobile_no = member.mobile_no
    
    def update_from_loan_product(self):
        loan_product = LoanProduct.objects.filter(loan_product_name=self.loan_product_name).first()
        if loan_product:
            self.interest_rate = loan_product.interest_rate
            self.payment_frequency = loan_product.mobile_no
            self.loan_term = loan_product.mobile_no
            
            


    class Meta:
        ordering = ['-updated', '-application_date']


    def __str__(self):
        return self.loan_id

  