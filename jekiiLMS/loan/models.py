from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.db.models import Sum
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils.timezone import now
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
    loan_id =models.CharField(max_length=50, null=True, unique=True)
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='loans_as_member')
    applied_amount = models.IntegerField()
    guarantor = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='loans_as_guarantor')
    application_date = models.DateField()
    loan_officer = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    loan_purpose = models.TextField()
    status = models.CharField(max_length=50, choices=LOAN_STATUS, default='pending')
    attachments = models.FileField(upload_to='attachments', null=True, blank=True)

    # Generate loan ID based on member ID and current timestamp
    def save(self, *args, **kwargs):
        if not self.loan_id:
            member_id = str(self.member_id).zfill(6)
            date_str = now().strftime('%Y%m%d')
            last_loan = Loan.objects.filter(loan_id__startswith=member_id+date_str).last()
            if last_loan:
                last_id = last_loan.loan_id[-4:]
                next_id = str(int(last_id)+1).zfill(4)
                self.loan_id = member_id+date_str+next_id
            else:
                self.loan_id = member_id+date_str+'0001'
        super(Loan, self).save(*args, **kwargs)
    


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

# Note models starts here   
class Note(models.Model):
    loan =models.ForeignKey(Loan, on_delete=models.CASCADE)
    body= models.TextField()
    author= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add= True)
 

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[0:50]

#Note model ends

# Repayment models starts here   
class Repayment(models.Model):
    transaction_id = models.CharField(max_length=20)
    loan_id = models.ForeignKey(Loan, on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    amount= models.IntegerField()
    date_paid = models.DateField()


    class Meta:
        ordering = ['-date_paid']

    def __str__(self):
        return self.transaction_id

    

    def loanBalance(self):
        loan = Loan.objects.get(pk=self.loan_id.pk)
        loan_repayments = Repayment.objects.filter(loan_id=self.loan_id).aggregate(Sum('amount'))['amount__sum']
        total_payable = loan.total_payable()
        loan_balance = total_payable - loan_repayments
        return loan_balance

    #method to calculate next_repayment_date
    def next_repayment_date(self):
        if self.loan_id.loan_product.repayment_frequency == 'weekly':
            return self.date_paid + timedelta(days=7)
        elif self.loan_id.loan_product.repayment_frequency == 'monthly':
            return self.date_paid + timedelta(days=30)
        else: 
            return self.date_paid + timedelta(days=1)
        



    

#Repayment model ends