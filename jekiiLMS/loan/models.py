from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.db.models import Sum
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.utils.timezone import now
from django.db import transaction
from member.models import Member
from company.models import Organization
from user.models import CompanyStaff
 

#Loan Prouct model starts here

REPAYMENT_FREQUENCY_CHOICES = (
    ('onetime','ONETIME'),
    ('daily', 'DAILY'),
    ('weekly','WEEKLY'),
    ('monthly','MONTHLY'),
)

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
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)
    loan_product_name = models.CharField(max_length=300)
    minimum_amount = models.IntegerField(default=5000)
    maximum_amount = models.IntegerField(default=10000)
    loan_product_term = models.IntegerField()
    loan_term_period= models.CharField(max_length=20, choices=TERM_PERIOD, default='month')
    repayment_frequency = models.CharField(max_length=8, choices=REPAYMENT_FREQUENCY_CHOICES, default='onetime')
    interest_type = models.CharField(max_length=30, choices=INTEREST_TYPE_CHOICES, default='flat_rate')
    #interest_rate = models.FloatField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    interest_rate = models.FloatField()
    service_fee_type = models.CharField(max_length=300, choices=SERVICE_FEE_TYPE_CHOICES, default='fixed_value')
    service_fee_value = models.FloatField()
    penalty_type = models.CharField(max_length=300, choices=PENALTY_FEE_TYPE_CHOICES, default='fixed_value')
    penalty_value = models.FloatField()
    penalty_frequency = models.CharField(max_length=300, choices=PENALTY_FREQUENCY_TYPE_CHOICES, default='fixed_value')
    status = models.CharField(max_length=10, choices=ACTIVE_CHOICES, default='active')
    loan_product_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.loan_product_name



#Loan  model starts here

LOAN_STATUS = (
    ('pending','PENDING'),
    ('approved','APPROVED'),
    ('rejected','REJECTED'),
    ('overdue','OVERDUE'),
    ('cleared','CLEARED'),
)
class Loan(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)
    loan_id =models.CharField(max_length=50, null=True, unique=True, blank=True)
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='loans_as_member')
    applied_amount = models.IntegerField()
    guarantor = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='loans_as_guarantor', blank=True)
    application_date = models.DateField()
    loan_officer = models.ForeignKey(CompanyStaff,on_delete=models.SET_NULL, null=True)
    loan_purpose = models.TextField()
    status = models.CharField(max_length=50, choices=LOAN_STATUS, default='pending')
    attachments = models.FileField(upload_to='loan_attachments/', null=True, blank=True)  
   


    #Generating loan id based on date 
    def save(self, *args, **kwargs):
        if not self.loan_id:
            date_str = now().strftime('%Y%m%d')
            #averting race condition using 'select_for_update()'
            with transaction.atomic():
                last_loan = Loan.objects.select_for_update().filter(loan_id__startswith=date_str).order_by('-loan_id').first()
                if last_loan:
                    last_id = last_loan.loan_id[-5:]
                    next_id = str(int(last_id)+1).zfill(5)
                    self.loan_id = date_str+next_id
                else:
                    self.loan_id = date_str+'00001'
        super(Loan, self).save(*args, **kwargs)

    #method to limit the application date input to be today or earlier date
    def clean(self):
        if self.application_date > now().date():
            raise ValidationError('Application date cannot be in the future.')


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
            

    class Meta:
        ordering = ['-application_date']


    def __str__(self):
        return self.loan_id

# Note models starts here   
class Note(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    loan =models.ForeignKey(Loan, on_delete=models.CASCADE, null=True)
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
    company = models.ForeignKey(Organization, on_delete=models.CASCADE)
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
        if self.loan_id:
            loan = Loan.objects.get(pk=self.loan_id.pk)
            loan_repayments = Repayment.objects.filter(loan_id=self.loan_id).aggregate(Sum('amount'))['amount__sum']
            total_payable = loan.total_payable()
            loan_balance = total_payable - loan_repayments
            return loan_balance

    #method to calculate next_repayment_date
    def next_repayment_date(self):
        if self.loan_id:
            if self.loan_id.loan_product.repayment_frequency == 'weekly':
                return self.date_paid + timedelta(days=7)
            elif self.loan_id.loan_product.repayment_frequency == 'monthly':
                return self.date_paid + timedelta(days=30)
            else: 
                return self.date_paid + timedelta(days=1)
        
    

#Repayment model ends 

#Guarantor Model starts
class Guarantor(models.Model):
    company =models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    loan =models.ForeignKey(Loan, on_delete=models.CASCADE, related_name = 'loan_as_no')
    name= models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    amount= models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
 

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.name)

#Collateral Model starts
TYPE = (
    ('electronics','ELECTRONICS'),
    ('vehicle','VEHICLE'),
    ('land','LAND'),
    ('shares','SHARES'),
    ('cash deposit','CASH DEPOSIT'),
    ('others','OTHERS'),
)
class Collateral(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    loan = models.ForeignKey(Loan, on_delete= models.CASCADE, null=True)
    name =models.CharField(max_length=20)
    type= models.CharField(max_length=50, choices=TYPE, default='others')
    serial_number= models.CharField(max_length=20)
    estimated_value = models.IntegerField()
 

    def __str__(self):
        return self.name  