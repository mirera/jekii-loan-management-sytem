from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
import uuid
from member.models import Member



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
    ('flat rate','FLAT RATE'),
    ('reducing balance', 'REDUCING BALANCE'),
)

SERVICE_FEE_TYPE_CHOICES = (
    ('fixed value','FIXED VALUE'),
    ('percentage of principal', 'p.c of Principal'),
)

PENALTY_FEE_TYPE_CHOICES = (
    ('fixed_value','FIXED VALUE'),
    ('percentage of principal', 'p.c of Due Principal'),
    ('percentage of principal interest', 'p.c of Due P + I'),
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

LOAN_STATUS = (
    ('pending','PENDING'),
    ('approved','APPROVED'),
    ('cancelled','CANCELLED'),
    ('overdue','OVERDUE'),
    ('cleared','CLEARED'),
)
class Loan(models.Model):
    loan_id =models.CharField(max_length=500, null=True, unique=True)
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='loans_as_member')
    applied_amount = models.IntegerField()
    guarantor = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='loans_as_guarantor')
    application_date = models.DateField()
    loan_officer = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    loan_purpose = models.TextField()
    status = models.CharField(max_length=50, choices=LOAN_STATUS, default='pending')
    attachments = models.FileField(upload_to='attachments', null=True, blank=True)

    #method to calculate first_repayment_date
    def first_repayment_date(self):
        if self.loan_product.repayment_frequency == 'weekly':
            return self.application_date + timedelta(days=7)
        elif self.loan_product.repayment_frequency == 'monthly':
            return self.application_date + timedelta(days=30)
        else:
            return self.application_date  # for daily repayment frequency

    
    # method to calculate total_payable
    def total_payable(self):
        principal = self.applied_amount
        interest_rate = self.loan_product.interest_rate
        penalty_value = self.loan_product.penalty_value

        interest = 0

        if self.loan_product.interest_type == 'flat_rate':
            interest = principal * interest_rate
        elif self.loan_product.interest_type == 'reducing_balance':
            interest = (principal * interest_rate * self.loan_product.loan_product_term) / 100

        if self.loan_product.penalty_type == 'fixed_value':
            penalty_fee = penalty_value
        elif self.loan_product.penalty_type == 'percentage of principal':
            penalty_fee = (principal * penalty_value) / 100
        elif self.loan_product.penalty_type == 'percentage of principal interest':
            penalty_fee = (principal + interest) * penalty_value / 100

        total_payable = principal + interest + penalty_fee

        return total_payable


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
        ordering = ['application_date']


    def __str__(self):
        return self.loan_id

    